#!/usr/bin/env python3
"""Build a fail-closed analysis for the Qwen3 v4 BFCL zero-score artifact."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS_DIR = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/"
    "qwen3-v4-peft-official-bfcl-20260616/results/"
    "Qwen_Qwen3-4B-Instruct-2507-FC/non_live"
)
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-bfcl-zero-score-failure-analysis-20260624.json"
DEFAULT_MD = DEFAULT_JSON.with_suffix(".md")
UPSTREAM_MARKERS = (
    "Error during inference",
    "Error code: 502",
    "Connection refused",
    "upstream request failed",
    "InternalServerError",
)
TOOL_CALL_MARKERS = ("<tool_call>", '"name"', '"arguments"', "'name'", "'arguments'")


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return rows


def category_from_path(path: Path) -> str:
    name = path.name.removesuffix("_result.json")
    return name.removeprefix("BFCL_v4_")


def classify_result(row: dict) -> str:
    result = str(row.get("result", ""))
    traceback = str(row.get("traceback", ""))
    combined = result + "\n" + traceback
    if any(marker in combined for marker in UPSTREAM_MARKERS):
        return "upstream_error"
    if result.strip() == "":
        return "blank_output"
    if any(marker in result for marker in TOOL_CALL_MARKERS):
        return "tool_call_like"
    return "other_completed"


def analyze_results(results_dir: Path) -> dict:
    if not results_dir.exists():
        raise FileNotFoundError(f"missing BFCL results dir: {results_dir}")

    files = sorted(results_dir.glob("BFCL_v4_*_result.json"))
    if not files:
        raise FileNotFoundError(f"no BFCL result files found in {results_dir}")

    categories: dict[str, dict] = {}
    aggregate = Counter()
    samples: dict[str, list[dict]] = {key: [] for key in ("upstream_error", "blank_output", "tool_call_like", "other_completed")}

    for path in files:
        category = category_from_path(path)
        rows = read_jsonl(path)
        counts = Counter(classify_result(row) for row in rows)
        aggregate.update(counts)
        categories[category] = {
            "path": str(path),
            "rows": len(rows),
            "counts": dict(sorted(counts.items())),
            "sample_ids": {
                label: [str(row.get("id", "")) for row in rows if classify_result(row) == label][:5]
                for label in ("upstream_error", "blank_output", "tool_call_like", "other_completed")
            },
        }
        for row in rows:
            label = classify_result(row)
            if len(samples[label]) >= 5:
                continue
            samples[label].append(
                {
                    "id": row.get("id"),
                    "category": category,
                    "result_preview": str(row.get("result", "")).replace("\n", "\\n")[:240],
                }
            )

    total_rows = sum(item["rows"] for item in categories.values())
    contaminated_rows = aggregate["upstream_error"] + aggregate["blank_output"]
    status = "blocked-clean-regeneration-required" if contaminated_rows else "clean-output-ready-for-model-quality-analysis"
    return {
        "report_id": "qwen3-v4-bfcl-zero-score-failure-analysis-20260624",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "results_dir": str(results_dir),
        "status": status,
        "summary": {
            "files": len(files),
            "categories": sorted(categories),
            "total_rows": total_rows,
            "counts": dict(sorted(aggregate.items())),
            "contaminated_rows": contaminated_rows,
            "contaminated_fraction": round(contaminated_rows / total_rows, 6) if total_rows else 0.0,
        },
        "categories": categories,
        "samples": samples,
        "gate": {
            "promotable": False,
            "reason": "The current BFCL zero-score artifact contains upstream endpoint failures and/or blank generations; regenerate clean outputs before using the score as model-quality evidence.",
            "rerun_contract": [
                "Start a fresh OpenAI-compatible endpoint and keep it reachable for the entire run.",
                "Write to a new BFCL output root or pass --allow-overwrite after archiving stale artifacts.",
                "Use low concurrency first, e.g. --num-threads 1, to avoid local proxy overload.",
                "Preserve endpoint/proxy logs with the score artifact.",
                "Only promote BFCL evidence when upstream_error_rows == 0 and blank_output_rows == 0.",
            ],
        },
    }


def write_markdown(report: dict, path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# Qwen3 v4 BFCL Zero-Score Failure Analysis",
        "",
        f"- Status: `{report['status']}`",
        f"- Result root: `{report['results_dir']}`",
        f"- Total rows: {summary['total_rows']}",
        f"- Upstream errors: {summary['counts'].get('upstream_error', 0)}",
        f"- Blank outputs: {summary['counts'].get('blank_output', 0)}",
        f"- Tool-call-like outputs: {summary['counts'].get('tool_call_like', 0)}",
        f"- Contaminated rows: {summary['contaminated_rows']} ({summary['contaminated_fraction']:.2%})",
        "",
        "## Category Counts",
        "",
        "| Category | Rows | Upstream errors | Blank outputs | Tool-call-like | Other completed |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for category, item in sorted(report["categories"].items()):
        counts = item["counts"]
        lines.append(
            "| "
            + " | ".join(
                [
                    category,
                    str(item["rows"]),
                    str(counts.get("upstream_error", 0)),
                    str(counts.get("blank_output", 0)),
                    str(counts.get("tool_call_like", 0)),
                    str(counts.get("other_completed", 0)),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "This artifact is not promotable as model-quality evidence. Regenerate BFCL outputs cleanly before treating the selected-slice score as meaningful.",
            "",
            "Required rerun contract:",
        ]
    )
    lines.extend(f"- {item}" for item in report["gate"]["rerun_contract"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    report = analyze_results(args.results_dir)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, args.markdown_output)
    print(f"wrote {args.json_output}")
    print(f"wrote {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
