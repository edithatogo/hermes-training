#!/usr/bin/env python3
"""Summarize strict and runtime-normalized tool-call benchmark results."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{lineno}: expected object rows")
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no rows found")
    return rows


def rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def build_summary(rows: list[dict[str, Any]], results_path: Path, run_id: str) -> dict[str, Any]:
    cases = len(rows)
    strict_passed = sum(1 for row in rows if row.get("pass") is True)
    runtime_passed = sum(1 for row in rows if row.get("pass_after_empty_think_strip") is True)
    rescued_rows = [
        row for row in rows if row.get("strict_failure_rescued_by_empty_think_strip") is True
    ]
    residual_rows = [
        row
        for row in rows
        if row.get("pass") is not True and row.get("pass_after_empty_think_strip") is not True
    ]
    empty_think_rows = [row for row in rows if row.get("empty_think_stripped_response")]
    categories = Counter(str(row.get("category", "unknown")) for row in rows)
    strict_by_category = Counter(
        str(row.get("category", "unknown")) for row in rows if row.get("pass") is True
    )
    runtime_by_category = Counter(
        str(row.get("category", "unknown"))
        for row in rows
        if row.get("pass_after_empty_think_strip") is True
    )

    return {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "source_results": str(results_path),
        "cases": cases,
        "strict_passed": strict_passed,
        "strict_pass_rate": rate(strict_passed, cases),
        "runtime_normalized_passed": runtime_passed,
        "runtime_normalized_pass_rate": rate(runtime_passed, cases),
        "empty_think_prefix_cases": len(empty_think_rows),
        "strict_failures_rescued_by_runtime_normalization": len(rescued_rows),
        "strict_failures_rescued_by_runtime_normalization_ids": [row["id"] for row in rescued_rows],
        "residual_runtime_failure_count": len(residual_rows),
        "residual_runtime_failure_ids": [row["id"] for row in residual_rows],
        "category_breakdown": {
            category: {
                "cases": count,
                "strict_pass_rate": rate(strict_by_category[category], count),
                "runtime_normalized_pass_rate": rate(runtime_by_category[category], count),
            }
            for category, count in sorted(categories.items())
        },
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Runtime-Normalized Tool-Call Summary",
        "",
        f"- Run id: `{summary['run_id']}`",
        f"- Created at: `{summary['created_at']}`",
        f"- Source results: `{summary['source_results']}`",
        f"- Cases: `{summary['cases']}`",
        f"- Strict pass rate: `{summary['strict_pass_rate']:.3f}`",
        f"- Runtime-normalized pass rate: `{summary['runtime_normalized_pass_rate']:.3f}`",
        f"- Responses with leading empty-think wrapper: `{summary['empty_think_prefix_cases']}`",
        (
            "- Strict failures rescued by runtime normalization: "
            f"`{summary['strict_failures_rescued_by_runtime_normalization']}`"
        ),
        f"- Residual runtime failures: `{summary['residual_runtime_failure_count']}`",
        "",
        "Runtime normalization removes only empty leading Qwen-style `<think></think>` wrappers before Hermes parsing. It is integration evidence only and does not change the strict benchmark publication gate.",
        "",
        "## Category Breakdown",
        "",
        "| Category | Cases | Strict pass | Runtime-normalized pass |",
        "|---|---:|---:|---:|",
    ]
    for category, item in summary["category_breakdown"].items():
        lines.append(
            f"| {category} | {item['cases']} | {item['strict_pass_rate']:.3f} | {item['runtime_normalized_pass_rate']:.3f} |"
        )
    lines.extend(["", "## Residual Failures", ""])
    residual_ids = summary["residual_runtime_failure_ids"]
    if residual_ids:
        lines.extend(f"- `{case_id}`" for case_id in residual_ids)
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="Tool-call benchmark results.jsonl.")
    parser.add_argument("--run-id", help="Optional report run id.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for summary.json and summary.md.")
    args = parser.parse_args()

    rows = load_jsonl(args.results)
    run_id = args.run_id or f"runtime-normalized-toolcall-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    summary = build_summary(rows, args.results, run_id)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "summary.md").write_text(render_markdown(summary), encoding="utf-8")
    print(f"wrote {args.output_dir / 'summary.json'}")
    print(f"wrote {args.output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
