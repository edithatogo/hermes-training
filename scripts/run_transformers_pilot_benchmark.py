#!/usr/bin/env python3
"""Run lightweight pilot benchmarks against a local Hugging Face Transformers model."""
from __future__ import annotations

import argparse
import json
import os
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from run_endpoint_pilot_benchmark import render_summary, score_case
from run_tool_call_benchmark import (
    apply_user_prefix,
    build_generation_prompt,
    resolve_default_output_root,
    save_jsonl,
)


def ensure_storage_env() -> None:
    storage_root = os.environ.get("HERMES_STORAGE_ROOT")
    if not storage_root:
        storage_root = "/Volumes/PortableSSD" if Path("/Volumes/PortableSSD").is_dir() else str(Path.cwd() / ".local-storage")
        os.environ["HERMES_STORAGE_ROOT"] = storage_root

    defaults = {
        "HF_HOME": f"{storage_root}/huggingface",
        "HF_HUB_CACHE": f"{storage_root}/huggingface/hub",
        "HF_HUB_DISABLE_XET": "1",
        "HF_DATASETS_CACHE": f"{storage_root}/huggingface/datasets",
        "TRANSFORMERS_CACHE": f"{storage_root}/huggingface/transformers",
        "XDG_CACHE_HOME": f"{storage_root}/cache",
        "HERMES_EVAL_ROOT": f"{storage_root}/hermes-evals",
        "TMPDIR": f"{storage_root}/tmp",
    }
    for key, value in defaults.items():
        os.environ.setdefault(key, value)
    for key in ("HF_HUB_CACHE", "HF_DATASETS_CACHE", "TRANSFORMERS_CACHE", "XDG_CACHE_HOME", "HERMES_EVAL_ROOT", "TMPDIR"):
        Path(os.environ[key]).mkdir(parents=True, exist_ok=True)


def resolve_dtype(dtype: str) -> Any:
    if dtype == "auto":
        return "auto"
    if dtype == "float16":
        return torch.float16
    if dtype == "bfloat16":
        return torch.bfloat16
    if dtype == "float32":
        return torch.float32
    raise ValueError(f"unsupported dtype: {dtype}")


def resolve_device(device: str) -> str:
    if device != "auto":
        return device
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def generate_transformers(
    model: Any,
    tokenizer: Any,
    messages: list[dict[str, Any]],
    device: str,
    max_tokens: int,
    assistant_prefill: str,
) -> tuple[str, float]:
    prompt = build_generation_prompt(messages, tokenizer, assistant_prefill)
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}
    started = time.time()
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=max_tokens,
            pad_token_id=tokenizer.eos_token_id,
        )
    new_tokens = output_ids[0, inputs["input_ids"].shape[-1] :]
    response = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return response.strip(), time.time() - started


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--user-prefix", default="")
    parser.add_argument("--assistant-prefill", default="")
    parser.add_argument("--require-no-extra-tool-text", action="store_true")
    parser.add_argument("--device", default="auto", help="auto, cpu, mps, or cuda")
    parser.add_argument("--dtype", choices=("auto", "float16", "bfloat16", "float32"), default="auto")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_storage_env()

    suite = json.loads(args.suite.read_text(encoding="utf-8"))
    if not isinstance(suite, list) or not suite:
        raise ValueError("suite must be a non-empty JSON array")

    run_id = args.run_id or f"transformers-pilot-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (
        resolve_default_output_root() / "standard-benchmarks" / "local-pilots" / run_id
    )
    device = resolve_device(args.device)
    dtype = resolve_dtype(args.dtype)

    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"categories: {dict(Counter(case['category'] for case in suite))}")
        print(f"model: {args.model}")
        print(f"device: {device}")
        print(f"dtype: {args.dtype}")
        print(f"local_files_only: {args.local_files_only}")
        print(f"trust_remote_code: {args.trust_remote_code}")
        print(f"output_dir: {output_dir}")
        return 0

    print(f"Loading tokenizer: {args.model}")
    tokenizer = AutoTokenizer.from_pretrained(
        args.model,
        local_files_only=args.local_files_only,
        trust_remote_code=args.trust_remote_code,
    )
    print(f"Loading model: {args.model}")
    started = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
        local_files_only=args.local_files_only,
        trust_remote_code=args.trust_remote_code,
    )
    model.to(device)
    model.eval()
    print(f"  loaded in {time.time() - started:.1f}s on {device}")

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    for index, case in enumerate(suite, 1):
        messages = case.get("messages")
        if not isinstance(messages, list):
            raise ValueError(f"{case.get('id', index)}: messages must be a list")
        print(f"  [{index}/{len(suite)}] {case['category']} {case['id']}")
        response, latency_s = generate_transformers(
            model,
            tokenizer,
            apply_user_prefix(messages, args.user_prefix),
            device,
            args.max_tokens,
            args.assistant_prefill,
        )
        scored = score_case(case, response, args.require_no_extra_tool_text)
        row = {
            "id": case["id"],
            "category": case["category"],
            "response": response,
            "latency_s": round(latency_s, 3),
            **scored,
        }
        rows.append(row)
        responses.append({"id": case["id"], "response": response, "latency_s": round(latency_s, 3)})

    passed = sum(1 for row in rows if row["pass"])
    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "model": args.model,
        "device": device,
        "dtype": args.dtype,
        "user_prefix": args.user_prefix,
        "assistant_prefill": args.assistant_prefill,
        "require_no_extra_tool_text": args.require_no_extra_tool_text,
        "output_dir": str(output_dir),
        "cases": len(rows),
        "passed": passed,
        "pass_rate": passed / len(rows),
    }
    save_jsonl(output_dir / "responses.jsonl", responses)
    save_jsonl(output_dir / "results.jsonl", rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_summary(summary, rows), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
