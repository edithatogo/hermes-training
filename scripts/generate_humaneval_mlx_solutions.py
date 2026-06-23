#!/usr/bin/env python3
"""Generate HumanEval/EvalPlus samples with a local MLX model and adapter."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "Qwen/Qwen3-4B-MLX-4bit"
DEFAULT_ADAPTER = "gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter"
DEFAULT_OUTPUT = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/"
    "qwen3-v4-peft-official-coding-20260616/generated.jsonl"
)
DEFAULT_SUMMARY = DEFAULT_OUTPUT.with_name("generation-summary.json")


def load_humaneval_problems() -> dict[str, dict[str, Any]]:
    from human_eval.data import read_problems

    return dict(read_problems())


def ordered_problem_items(problems: dict[str, dict[str, Any]]) -> list[tuple[str, dict[str, Any]]]:
    def sort_key(item: tuple[str, dict[str, Any]]) -> tuple[str, int]:
        task_id = item[0]
        prefix, _, number = task_id.partition("/")
        return prefix, int(number) if number.isdigit() else 10**9

    return sorted(problems.items(), key=sort_key)


def load_existing_task_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    task_ids: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if isinstance(row, dict) and row.get("task_id"):
                task_ids.add(str(row["task_id"]))
    return task_ids


def build_prompt(problem: dict[str, Any]) -> str:
    prompt = str(problem["prompt"]).rstrip()
    return (
        f"{prompt}\n\n"
        "Complete the Python function above. Return only the code that should be appended after the prompt. "
        "Do not include Markdown fences or explanatory text.\n"
    )


def clean_completion(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        stripped = "\n".join(lines).strip("\n")
    for marker in ("\n# Task", "\nif __name__ == \"__main__\":", "\n```"):
        if marker in stripped:
            stripped = stripped.split(marker, 1)[0].rstrip()
    return stripped.rstrip() + "\n"


def generate_completion(model: Any, tokenizer: Any, prompt: str, max_tokens: int) -> str:
    from mlx_lm import generate as mlx_generate

    response = mlx_generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)
    return clean_completion(str(response))


def write_summary(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--adapter", default=DEFAULT_ADAPTER)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--limit", type=int, help="Generate only the first N not-yet-present problems.")
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    problems = load_humaneval_problems()
    ordered = ordered_problem_items(problems)
    existing = load_existing_task_ids(args.output) if args.resume else set()
    pending = [(task_id, problem) for task_id, problem in ordered if task_id not in existing]
    if args.limit is not None:
        pending = pending[: args.limit]

    summary = {
        "model": args.model,
        "adapter": args.adapter,
        "output": str(args.output),
        "summary_output": str(args.summary_output),
        "total_problems": len(ordered),
        "existing_rows": len(existing),
        "pending_rows": len(pending),
        "limit": args.limit,
        "max_tokens": args.max_tokens,
        "status": "dry-run" if args.dry_run else "started",
        "generated_rows": 0,
        "duration_s": 0.0,
    }
    if args.dry_run:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    from mlx_lm import load

    started = time.time()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    model, tokenizer = load(args.model, adapter_path=args.adapter)
    mode = "a" if args.resume else "w"
    generated = 0
    with args.output.open(mode, encoding="utf-8") as handle:
        for task_id, problem in pending:
            completion = generate_completion(model, tokenizer, build_prompt(problem), args.max_tokens)
            handle.write(json.dumps({"task_id": task_id, "completion": completion}, sort_keys=True) + "\n")
            handle.flush()
            generated += 1
            summary.update(
                {
                    "status": "running",
                    "generated_rows": generated,
                    "last_task_id": task_id,
                    "duration_s": round(time.time() - started, 3),
                }
            )
            write_summary(args.summary_output, summary)
    summary.update({"status": "complete", "generated_rows": generated, "duration_s": round(time.time() - started, 3)})
    write_summary(args.summary_output, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
