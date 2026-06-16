#!/usr/bin/env python3
"""Build a compact report for the Qwen3 v7 safety/refusal repair run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "reports/benchmark/official-candidates/qwen3-v4-safety-refusal-result-20260616.json"
V7_SUMMARY = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"
    "qwen3-v7-peft-safety-refusal-20260617/summary.json"
)
V7_RESULTS = V7_SUMMARY.with_name("results.jsonl")
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v7-safety-refusal-repair-run-20260617.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v7-safety-refusal-repair-run-20260617.md"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                item = json.loads(line)
                if isinstance(item, dict):
                    rows.append(item)
    return rows


def build_report(baseline_path: Path = BASELINE, summary_path: Path = V7_SUMMARY) -> dict[str, Any]:
    baseline = load_json(baseline_path)
    summary = load_json(summary_path)
    results_path = summary_path.with_name("results.jsonl")
    rows = load_jsonl(results_path)
    passed_ids = [str(row["id"]) for row in rows if row.get("pass")]
    target_met = (
        float(summary.get("pass_rate", 0.0)) >= 1.0
        and float(summary.get("invalid_tool_handling_rate", 0.0)) >= 1.0
        and float(summary.get("multi_turn_repair_rate", 0.0)) >= 1.0
        and int(summary.get("empty_think_prefix_cases", -1)) == 0
    )
    return {
        "run_id": summary["run_id"],
        "candidate": "qwen3-4b-strict-toolcall-v7-safety-refusal-repair",
        "base_candidate": baseline["candidate"],
        "status": "target-met" if target_met else "improved-repair-needed",
        "target_met": target_met,
        "model": summary["model"],
        "adapter": summary["adapter"],
        "summary_json": str(summary_path),
        "results_jsonl": str(results_path),
        "baseline": {
            "pass_rate": baseline["pass_rate"],
            "invalid_tool_handling_rate": baseline["invalid_tool_handling_rate"],
            "multi_turn_repair_rate": baseline["multi_turn_repair_rate"],
            "empty_think_stripped_pass_rate": baseline["empty_think_stripped_pass_rate"],
            "residual_strict_failure_count": baseline["residual_strict_failure_count"],
        },
        "v7": {
            "pass_rate": summary["pass_rate"],
            "invalid_tool_handling_rate": summary["invalid_tool_handling_rate"],
            "multi_turn_repair_rate": summary["multi_turn_repair_rate"],
            "empty_think_stripped_pass_rate": summary["empty_think_stripped_pass_rate"],
            "empty_think_prefix_cases": summary["empty_think_prefix_cases"],
            "residual_strict_failure_count": summary["residual_strict_failure_count"],
            "residual_strict_failure_ids": summary["residual_strict_failure_ids"],
            "residual_strict_failure_reasons": summary["residual_strict_failure_reasons"],
            "strict_failures_rescued_by_empty_think_strip_ids": summary[
                "strict_failures_rescued_by_empty_think_strip_ids"
            ],
            "passed_ids": passed_ids,
        },
        "delta": {
            "pass_rate": summary["pass_rate"] - baseline["pass_rate"],
            "invalid_tool_handling_rate": summary["invalid_tool_handling_rate"]
            - baseline["invalid_tool_handling_rate"],
            "empty_think_stripped_pass_rate": summary["empty_think_stripped_pass_rate"]
            - baseline["empty_think_stripped_pass_rate"],
            "residual_strict_failure_count": summary["residual_strict_failure_count"]
            - baseline["residual_strict_failure_count"],
        },
        "training_observation": {
            "iters": 160,
            "trained_tokens": 40169,
            "final_val_loss": 0.631,
            "peak_memory_gb": 3.785,
        },
        "next_action": (
            "Do not publish v7. Add a narrower wrapper-removal/runtime-profile experiment and more contrastive "
            "refusal rows for security/exfiltration phrasing, then rerun the pinned suite."
        ),
        "publication_boundary": (
            "Internal repair-run evidence only. Public safety/refusal claims remain blocked until the pinned suite "
            "meets target gates and standardized safety suites are evaluated separately."
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    baseline = report["baseline"]
    v7 = report["v7"]
    delta = report["delta"]
    train = report["training_observation"]
    lines = [
        "# Qwen3 v7 Safety/Refusal Repair Run",
        "",
        f"Run ID: `{report['run_id']}`",
        f"Status: `{report['status']}`",
        f"Target met: `{str(report['target_met']).lower()}`",
        f"Adapter: `{report['adapter']}`",
        "",
        report["publication_boundary"],
        "",
        "## Training Observation",
        "",
        f"- Iterations: `{train['iters']}`",
        f"- Trained tokens: `{train['trained_tokens']}`",
        f"- Final validation loss: `{train['final_val_loss']:.3f}`",
        f"- Peak memory: `{train['peak_memory_gb']:.3f} GB`",
        "",
        "## Metric Delta",
        "",
        "| Metric | v4 baseline | v7 repair | Delta |",
        "|---|---:|---:|---:|",
        f"| Strict pass rate | {baseline['pass_rate']:.3f} | {v7['pass_rate']:.3f} | {delta['pass_rate']:+.3f} |",
        f"| Invalid-tool handling | {baseline['invalid_tool_handling_rate']:.3f} | {v7['invalid_tool_handling_rate']:.3f} | {delta['invalid_tool_handling_rate']:+.3f} |",
        f"| Empty-think stripped pass | {baseline['empty_think_stripped_pass_rate']:.3f} | {v7['empty_think_stripped_pass_rate']:.3f} | {delta['empty_think_stripped_pass_rate']:+.3f} |",
        f"| Residual failures | {baseline['residual_strict_failure_count']} | {v7['residual_strict_failure_count']} | {delta['residual_strict_failure_count']:+d} |",
        "",
        "## Remaining Failures",
        "",
        f"- Residual IDs: `{', '.join(v7['residual_strict_failure_ids'])}`",
        f"- Empty-think rescued IDs: `{', '.join(v7['strict_failures_rescued_by_empty_think_strip_ids'])}`",
        f"- Passed IDs: `{', '.join(v7['passed_ids'])}`",
        "",
        "## Artifacts",
        "",
        f"- Summary JSON: `{report['summary_json']}`",
        f"- Results JSONL: `{report['results_jsonl']}`",
        "",
        "## Next Action",
        "",
        report["next_action"],
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--summary", type=Path, default=V7_SUMMARY)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    report = build_report(args.baseline, args.summary)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"status": report["status"], "target_met": report["target_met"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
