#!/usr/bin/env python3
"""Run lightweight pilot benchmarks against a local MLX model or adapter."""
from __future__ import annotations

import argparse
import json
import os
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from run_endpoint_pilot_benchmark import apply_system_affixes, render_summary, score_case
from run_tool_call_benchmark import (
    apply_user_prefix,
    build_generation_prompt,
    extract_allowed_tools,
    normalize_granite_native_tool_calls,
    normalize_gemma_native_tool_calls,
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


def generate_local(
    model: Any,
    tokenizer: Any,
    messages: list[dict[str, Any]],
    max_tokens: int,
    assistant_prefill: str,
) -> tuple[str, float]:
    from mlx_lm import generate as mlx_generate

    prompt = build_generation_prompt(messages, tokenizer, assistant_prefill)
    started = time.time()
    response = mlx_generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)
    return response.strip(), time.time() - started


def build_scored_response(response: str, score_prefix: str = "", score_suffix: str = "") -> str:
    return f"{score_prefix}{response}{score_suffix}"


def apply_score_normalizer(response: str, normalizer: str, messages: list[dict[str, Any]]) -> str:
    if normalizer == "none":
        return response
    if normalizer == "gemma-native-tool-call":
        return normalize_gemma_native_tool_calls(response, extract_allowed_tools(messages))
    if normalizer == "granite-native-tool-call":
        return normalize_granite_native_tool_calls(response, extract_allowed_tools(messages))
    raise ValueError(f"unsupported score normalizer: {normalizer}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--adapter")
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--system-prefix", default="")
    parser.add_argument("--system-suffix", default="")
    parser.add_argument("--user-prefix", default="")
    parser.add_argument(
        "--assistant-prefill",
        default="",
        help="Optional assistant-side prefill appended to the generation prompt.",
    )
    parser.add_argument(
        "--score-prefix",
        default="",
        help="Optional text prepended to the generated response before scoring only; raw response is preserved.",
    )
    parser.add_argument(
        "--score-suffix",
        default="",
        help="Optional text appended to the generated response before scoring only; raw response is preserved.",
    )
    parser.add_argument(
        "--score-normalizer",
        choices=("none", "gemma-native-tool-call", "granite-native-tool-call"),
        default="none",
        help="Optional score-only runtime normalizer. Strict raw responses remain preserved.",
    )
    parser.add_argument("--require-no-extra-tool-text", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ensure_storage_env()

    suite = json.loads(args.suite.read_text(encoding="utf-8"))
    if not isinstance(suite, list) or not suite:
        raise ValueError("suite must be a non-empty JSON array")

    run_id = args.run_id or f"local-pilot-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (
        resolve_default_output_root() / "standard-benchmarks" / "local-pilots" / run_id
    )

    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"categories: {dict(Counter(case['category'] for case in suite))}")
        print(f"model: {args.model}")
        print(f"adapter: {args.adapter or '(none)'}")
        print(f"system_prefix: {args.system_prefix}")
        print(f"system_suffix: {args.system_suffix}")
        print(f"user_prefix: {args.user_prefix}")
        print(f"assistant_prefill: {args.assistant_prefill!r}")
        print(f"score_prefix: {args.score_prefix!r}")
        print(f"score_suffix: {args.score_suffix!r}")
        print(f"score_normalizer: {args.score_normalizer!r}")
        print(f"require_no_extra_tool_text: {args.require_no_extra_tool_text}")
        print(f"output_dir: {output_dir}")
        return 0

    print(f"Loading model: {args.model}")
    from mlx_lm import load

    started = time.time()
    model, tokenizer = load(args.model, adapter_path=args.adapter)
    print(f"  loaded in {time.time() - started:.1f}s")

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    for index, case in enumerate(suite, 1):
        messages = case.get("messages")
        if not isinstance(messages, list):
            raise ValueError(f"{case.get('id', index)}: messages must be a list")
        print(f"  [{index}/{len(suite)}] {case['category']} {case['id']}")
        response, latency_s = generate_local(
            model,
            tokenizer,
            apply_user_prefix(
                apply_system_affixes(messages, args.system_prefix, args.system_suffix),
                args.user_prefix,
            ),
            args.max_tokens,
            args.assistant_prefill,
        )
        normalized_for_score = apply_score_normalizer(response, args.score_normalizer, messages)
        scored_response = build_scored_response(normalized_for_score, args.score_prefix, args.score_suffix)
        scored = score_case(case, scored_response, args.require_no_extra_tool_text)
        row = {
            "id": case["id"],
            "category": case["category"],
            "response": response,
            "scored_response": scored_response if scored_response != response else "",
            "latency_s": round(latency_s, 3),
            **scored,
        }
        rows.append(row)
        response_row = {"id": case["id"], "response": response, "latency_s": round(latency_s, 3)}
        if scored_response != response:
            response_row["scored_response"] = scored_response
        responses.append(response_row)

    passed = sum(1 for row in rows if row["pass"])
    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "model": args.model,
        "adapter": args.adapter or "",
        "system_prefix": args.system_prefix,
        "system_suffix": args.system_suffix,
        "user_prefix": args.user_prefix,
        "assistant_prefill": args.assistant_prefill,
        "score_prefix": args.score_prefix,
        "score_suffix": args.score_suffix,
        "score_normalizer": args.score_normalizer,
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
