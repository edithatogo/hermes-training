#!/usr/bin/env python3
"""Run lightweight endpoint pilot benchmarks through an OpenAI-compatible API."""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from run_endpoint_tool_call_benchmark import apply_assistant_prefill, apply_user_prefix
from run_tool_call_benchmark import extract_tool_calls, save_jsonl


def chat(base_url: str, model: str, messages: list[dict[str, str]], max_tokens: int, timeout_s: float) -> tuple[str, float]:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": False,
    }
    started = time.time()
    response = requests.post(base_url.rstrip("/") + "/chat/completions", json=payload, timeout=timeout_s)
    latency_s = time.time() - started
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip(), latency_s


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def json_from_response(response: str) -> Any:
    stripped = response.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 2 and lines[-1].strip() == "```":
            stripped = "\n".join(lines[1:-1]).strip()
    return json.loads(stripped)


def score_case(case: dict[str, Any], response: str) -> dict[str, Any]:
    expected = case["expected"]
    category = case["category"]
    normalized_response = normalize_text(response)

    if category == "json_exact":
        try:
            parsed = json_from_response(response)
        except Exception as exc:
            return {"pass": False, "reason": f"invalid json: {exc}"}
        passed = parsed == expected["json"]
        return {"pass": passed, "reason": "" if passed else "json did not exactly match", "parsed_json": parsed}

    if category == "line_count":
        lines = [line for line in response.splitlines() if line.strip()]
        count_ok = len(lines) == int(expected["line_count"])
        prefix = expected.get("line_prefix")
        prefix_ok = True if prefix is None else all(line.startswith(prefix) for line in lines)
        passed = count_ok and prefix_ok
        return {
            "pass": passed,
            "reason": "" if passed else f"line_count={len(lines)} prefix_ok={prefix_ok}",
            "line_count": len(lines),
            "prefix_ok": prefix_ok,
        }

    if category in {"contains_excludes", "code_contains"}:
        contains_all = [normalize_text(item) for item in expected.get("contains_all", [])]
        contains_any = [normalize_text(item) for item in expected.get("contains_any", [])]
        excludes_any = [normalize_text(item) for item in expected.get("excludes_any", [])]
        all_ok = all(item in normalized_response for item in contains_all)
        any_ok = True if not contains_any else any(item in normalized_response for item in contains_any)
        excludes_ok = all(item not in normalized_response for item in excludes_any)
        passed = all_ok and any_ok and excludes_ok
        return {
            "pass": passed,
            "reason": "" if passed else f"all_ok={all_ok} any_ok={any_ok} excludes_ok={excludes_ok}",
            "all_ok": all_ok,
            "any_ok": any_ok,
            "excludes_ok": excludes_ok,
        }

    if category == "tool_call_exact":
        calls, errors, _ = extract_tool_calls(response)
        passed = calls == expected["tool_calls"]
        return {
            "pass": passed,
            "reason": "" if passed else "tool calls did not exactly match",
            "tool_calls": calls,
            "parse_errors": errors,
        }

    raise ValueError(f"unsupported pilot category: {category}")


def render_summary(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    by_category = Counter(row["category"] for row in rows)
    passed_by_category = Counter(row["category"] for row in rows if row["pass"])
    lines = [
        "# Pilot Benchmark Summary",
        "",
        f"- Run id: `{summary['run_id']}`",
        f"- Suite: `{summary['suite']}`",
        f"- Model: `{summary['model']}`",
        f"- Cases: `{summary['cases']}`",
        f"- Pass rate: `{summary['pass_rate']:.3f}`",
        f"- Output root: `{summary['output_dir']}`",
        "",
        "## Category Breakdown",
        "",
        "| Category | Cases | Pass rate |",
        "|---|---:|---:|",
    ]
    if summary.get("base_url"):
        lines.insert(6, f"- Base URL: `{summary['base_url']}`")
    if summary.get("adapter"):
        lines.insert(6, f"- Adapter: `{summary['adapter']}`")
    for category in sorted(by_category):
        lines.append(
            f"| {category} | {by_category[category]} | {passed_by_category[category] / by_category[category]:.3f} |"
        )
    failures = [row for row in rows if not row["pass"]]
    if failures:
        lines.extend(["", "## Failures", ""])
        for row in failures:
            lines.append(f"- `{row['id']}`: {row.get('reason', '')}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--timeout-s", type=float, default=120)
    parser.add_argument("--user-prefix", default="")
    parser.add_argument(
        "--assistant-prefill",
        default="",
        help="Optional assistant-side prefill appended as the final assistant message for compatible endpoints.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = json.loads(args.suite.read_text(encoding="utf-8"))
    if not isinstance(suite, list) or not suite:
        raise ValueError("suite must be a non-empty JSON array")
    run_id = args.run_id or f"endpoint-pilot-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or Path("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots") / run_id

    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"categories: {dict(Counter(case['category'] for case in suite))}")
        print(f"output_dir: {output_dir}")
        print(f"user_prefix: {args.user_prefix}")
        print(f"assistant_prefill: {args.assistant_prefill!r}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    for index, case in enumerate(suite, 1):
        print(f"  [{index}/{len(suite)}] {case['category']} {case['id']}")
        response, latency_s = chat(
            args.base_url,
            args.model,
            apply_assistant_prefill(apply_user_prefix(case["messages"], args.user_prefix), args.assistant_prefill),
            args.max_tokens,
            args.timeout_s,
        )
        scored = score_case(case, response)
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
        "base_url": args.base_url,
        "model": args.model,
        "user_prefix": args.user_prefix,
        "assistant_prefill": args.assistant_prefill,
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
    sys.exit(main())
