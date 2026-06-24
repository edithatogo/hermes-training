#!/usr/bin/env python3
"""Build a report for the Qwen3 v4 BFCL clean-rerun attempt."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ROOT = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/"
    "qwen3-v4-peft-official-bfcl-clean-rerun-20260624"
)
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-bfcl-clean-rerun-20260624.json"
DEFAULT_MD = DEFAULT_JSON.with_suffix(".md")
UPSTREAM_MARKERS = (
    "Error during inference",
    "Error code: 502",
    "Connection refused",
    "upstream request failed",
    "InternalServerError",
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return rows


def classify_result(row: dict[str, Any]) -> str:
    result = str(row.get("result", ""))
    traceback = str(row.get("traceback", ""))
    combined = result + "\n" + traceback
    if any(marker in combined for marker in UPSTREAM_MARKERS):
        return "upstream_error"
    if result.strip() == "":
        return "blank_output"
    return "completed_output"


def read_overall_score(score_csv: Path) -> dict[str, str]:
    if not score_csv.exists():
        return {}
    with score_csv.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[0] if rows else {}


def build_report(run_root: Path) -> dict[str, Any]:
    result_root = run_root / "results/Qwen_Qwen3-4B-Instruct-2507-FC/non_live"
    if not result_root.exists():
        raise FileNotFoundError(f"missing result root: {result_root}")
    files = sorted(result_root.glob("BFCL_v4_*_result.json"))
    if not files:
        raise FileNotFoundError(f"no BFCL result files under {result_root}")

    categories: dict[str, dict[str, Any]] = {}
    aggregate: Counter[str] = Counter()
    for path in files:
        category = path.name.removeprefix("BFCL_v4_").removesuffix("_result.json")
        rows = read_jsonl(path)
        counts = Counter(classify_result(row) for row in rows)
        aggregate.update(counts)
        categories[category] = {
            "path": str(path),
            "rows": len(rows),
            "counts": dict(sorted(counts.items())),
            "sample_ids": [str(row.get("id", "")) for row in rows[:10]],
            "sample_outputs": [str(row.get("result", "")).replace("\n", "\\n")[:160] for row in rows[:3]],
        }

    total_rows = sum(item["rows"] for item in categories.values())
    upstream_rows = int(aggregate.get("upstream_error", 0))
    blank_rows = int(aggregate.get("blank_output", 0))
    completed_rows = int(aggregate.get("completed_output", 0))
    if upstream_rows:
        status = "blocked-upstream-error-gate"
        gate_reason = "Clean rerun still contains upstream endpoint/proxy errors."
    elif blank_rows:
        status = "blocked-blank-output-gate"
        gate_reason = "Clean rerun has no upstream errors, but generated blank model outputs."
    elif total_rows < 800:
        status = "blocked-incomplete-selected-slice"
        gate_reason = "Clean rerun has no upstream or blank outputs, but selected-slice generation is incomplete."
    else:
        status = "clean-selected-slice-ready-for-score-review"
        gate_reason = "Clean rerun contains no upstream errors or blank outputs."

    return {
        "report_id": "qwen3-v4-bfcl-clean-rerun-20260624",
        "created_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "candidate": "qwen3-4b-strict-toolcall-v4-targeted",
        "suite": "official-bfcl",
        "scope": "selected official BFCL categories; clean rerun stopped after blank-output gate failure",
        "run_root": str(run_root),
        "status": status,
        "summary": {
            "files": len(files),
            "categories": sorted(categories),
            "total_rows": total_rows,
            "upstream_error_rows": upstream_rows,
            "blank_output_rows": blank_rows,
            "completed_output_rows": completed_rows,
            "overall_acc": read_overall_score(run_root / "scores/data_overall.csv").get("Overall Acc", ""),
        },
        "categories": categories,
        "logs": {
            "mlx_server": str(run_root / "logs/mlx-server-8097.log"),
            "proxy": str(run_root / "logs/openai-normalizing-proxy-8098.log"),
            "generate": str(run_root / "logs/bfcl-generate-simple-multiple-parallel-clean.log"),
            "evaluate": str(run_root / "logs/bfcl-evaluate-multiple-clean-partial.log"),
        },
        "gate": {
            "passed": status == "clean-selected-slice-ready-for-score-review",
            "reason": gate_reason,
            "required_before_model_quality_claim": [
                "upstream_error_rows == 0",
                "blank_output_rows == 0",
                "complete selected-slice generation or an explicit narrower smoke scope",
            ],
        },
        "publication_boundary": "Evidence-only clean-rerun attempt. Not a full BFCL claim and not sufficient for model publication.",
        "next_action": "Repair blank BFCL completion behavior before another selected-slice regeneration; keep endpoint/proxy command shape because upstream errors were cleared.",
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Qwen3 v4 BFCL Clean Rerun",
        "",
        f"- Status: `{report['status']}`",
        f"- Run root: `{report['run_root']}`",
        f"- Total generated rows: `{summary['total_rows']}`",
        f"- Upstream-error rows: `{summary['upstream_error_rows']}`",
        f"- Blank-output rows: `{summary['blank_output_rows']}`",
        f"- Completed-output rows: `{summary['completed_output_rows']}`",
        f"- Overall accuracy: `{summary['overall_acc'] or 'N/A'}`",
        "",
        "## Category Counts",
        "",
        "| Category | Rows | Upstream errors | Blank outputs | Completed outputs |",
        "|---|---:|---:|---:|---:|",
    ]
    for category, item in sorted(report["categories"].items()):
        counts = item["counts"]
        lines.append(
            f"| `{category}` | {item['rows']} | {counts.get('upstream_error', 0)} | "
            f"{counts.get('blank_output', 0)} | {counts.get('completed_output', 0)} |"
        )
    lines.extend(
        [
            "",
            "## Gate",
            "",
            f"- Passed: `{str(report['gate']['passed']).lower()}`",
            f"- Reason: {report['gate']['reason']}",
            "",
            "## Boundary",
            "",
            report["publication_boundary"],
            "",
            "## Next Action",
            "",
            report["next_action"],
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    report = build_report(args.run_root)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(f"wrote {args.json_output}")
    print(f"wrote {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
