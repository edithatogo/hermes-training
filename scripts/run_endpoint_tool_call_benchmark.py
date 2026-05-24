#!/usr/bin/env python3
"""Run the local tool-call benchmark through an OpenAI-compatible endpoint."""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from run_tool_call_benchmark import (
    apply_user_prefix,
    load_json,
    render_summary_markdown,
    resolve_default_output_root,
    save_jsonl,
    score_case,
    validate_suite,
)


def endpoint_chat(
    base_url: str,
    model: str,
    messages: list[dict[str, Any]],
    max_tokens: int,
    timeout_s: float,
) -> tuple[str, float]:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": False,
    }
    t0 = time.time()
    response = requests.post(url, json=payload, timeout=timeout_s)
    latency_s = time.time() - t0
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("endpoint response did not include choices[]")
    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise ValueError("endpoint response did not include choices[0].message.content")
    return message["content"].strip(), latency_s


def build_summary(
    run_id: str,
    suite: Path,
    output_dir: Path,
    base_url: str,
    model: str,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    cases = len(rows)
    passed = sum(1 for row in rows if row["pass"])
    tool_call_rows = [row for row in rows if row.get("expected_mode") == "tool_calls"]
    json_valid_count = sum(1 for row in tool_call_rows if row["json_valid"])
    arg_correct_count = sum(1 for row in tool_call_rows if row.get("arguments_correct"))
    normalized_passed = sum(1 for row in rows if row.get("pass_after_empty_think_strip"))
    normalized_json_valid_count = sum(
        1 for row in tool_call_rows if row.get("json_valid_after_empty_think_strip")
    )
    normalized_arg_correct_count = sum(
        1 for row in tool_call_rows if row.get("arguments_correct_after_empty_think_strip")
    )
    invalid_tool_rows = [row for row in rows if row["category"] == "invalid_tool_handling"]
    invalid_tool_ok_count = sum(1 for row in invalid_tool_rows if row["pass"])
    repair_rows = [row for row in rows if row["category"] == "multi_turn_repair"]
    repair_ok_count = sum(1 for row in repair_rows if row["pass"])
    empty_think_prefix_rows = [row for row in rows if row.get("empty_think_stripped_response")]
    empty_think_rescued_rows = [
        row for row in rows if row.get("strict_failure_rescued_by_empty_think_strip")
    ]
    residual_failure_rows = [
        row
        for row in rows
        if not row["pass"] and not row.get("strict_failure_rescued_by_empty_think_strip")
    ]

    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(suite),
        "output_dir": str(output_dir),
        "base_url": base_url,
        "model": model,
        "adapter": "(endpoint)",
        "cases": cases,
        "tool_call_cases": len(tool_call_rows),
        "passed": passed,
        "pass_rate": passed / cases,
        "json_valid_rate": json_valid_count / max(1, len(tool_call_rows)),
        "argument_accuracy_rate": arg_correct_count / max(1, len(tool_call_rows)),
        "empty_think_stripped_pass_rate": normalized_passed / cases,
        "empty_think_stripped_json_valid_rate": normalized_json_valid_count / max(1, len(tool_call_rows)),
        "empty_think_stripped_argument_accuracy_rate": normalized_arg_correct_count / max(1, len(tool_call_rows)),
        "empty_think_prefix_cases": len(empty_think_prefix_rows),
        "strict_failures_rescued_by_empty_think_strip": len(empty_think_rescued_rows),
        "strict_failures_rescued_by_empty_think_strip_ids": [row["id"] for row in empty_think_rescued_rows],
        "residual_strict_failure_count": len(residual_failure_rows),
        "residual_strict_failure_ids": [row["id"] for row in residual_failure_rows],
        "residual_strict_failure_reasons": {
            row["id"]: row.get("reason", "") for row in residual_failure_rows
        },
        "invalid_tool_handling_rate": invalid_tool_ok_count / max(1, len(invalid_tool_rows)),
        "multi_turn_repair_rate": repair_ok_count / max(1, len(repair_rows)),
    }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:11434/v1")
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--suite",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "benchmarks" / "tool_call_local" / "suite.json",
    )
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--user-prefix", default="")
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = load_json(args.suite)
    if not isinstance(suite, list):
        raise ValueError(f"{args.suite}: expected a JSON array of benchmark cases")
    validate_suite(suite, args.suite)

    run_id = args.run_id or f"endpoint-toolcall-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (resolve_default_output_root() / "endpoint-tool-call-benchmark" / run_id)

    if args.dry_run:
        categories = Counter(str(case.get("category", "unknown")) for case in suite)
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"categories: {dict(categories)}")
        print(f"base_url: {args.base_url}")
        print(f"model: {args.model}")
        print(f"output_dir: {output_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    response_rows: list[dict[str, Any]] = []
    for index, case in enumerate(suite, 1):
        messages = case.get("messages", [])
        if not isinstance(messages, list):
            raise ValueError(f"{case['id']}: messages must be a list")
        print(f"  [{index}/{len(suite)}] {case.get('category', 'unknown')} {case['id']}")
        response, latency_s = endpoint_chat(
            args.base_url,
            args.model,
            apply_user_prefix(messages, args.user_prefix),
            args.max_tokens,
            args.timeout_s,
        )
        response_rows.append({"id": case["id"], "response": response, "latency_s": round(latency_s, 3)})
        rows.append(
            {
                "id": case["id"],
                "category": case.get("category", "unknown"),
                "response": response,
                "latency_s": round(latency_s, 3),
                **score_case(case, response),
            }
        )

    summary = build_summary(run_id, args.suite, output_dir, args.base_url, args.model, rows)
    save_jsonl(output_dir / "responses.jsonl", response_rows)
    save_jsonl(output_dir / "results.jsonl", rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_summary_markdown(summary, rows), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"results: {output_dir / 'results.jsonl'}")
    print(f"summary: {output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
