#!/usr/bin/env python3
"""Build the Qwen3 v9 runtime refusal-marker normalization proof report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
V9_RAW_REPORT = ROOT / "reports/benchmark/official-candidates/qwen3-v9-runtime-profile-refusal-marker-repair-run-20260624.json"
NORMALIZED_SUMMARY = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"
    "qwen3-v9-runtime-profile-refusal-marker-normalized-20260624/summary.json"
)
NORMALIZED_INPUT = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"
    "qwen3-v9-runtime-profile-refusal-marker-normalized-input-20260624/responses.jsonl"
)
NORMALIZED_CHANGES = NORMALIZED_INPUT.with_name("changes.json")
DEFAULT_JSON = (
    ROOT / "reports/benchmark/official-candidates/"
    "qwen3-v9-runtime-refusal-marker-normalization-proof-20260624.json"
)
DEFAULT_MD = DEFAULT_JSON.with_suffix(".md")


def load_json(path: Path) -> dict[str, Any] | list[Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report(
    raw_report_path: Path = V9_RAW_REPORT,
    normalized_summary_path: Path = NORMALIZED_SUMMARY,
    normalized_input_path: Path = NORMALIZED_INPUT,
    changes_path: Path = NORMALIZED_CHANGES,
) -> dict[str, Any]:
    raw_report = load_json(raw_report_path)
    summary = load_json(normalized_summary_path)
    changes = load_json(changes_path)
    if not isinstance(raw_report, dict) or not isinstance(summary, dict) or not isinstance(changes, list):
        raise ValueError("unexpected report input shape")
    raw = raw_report["v9"]
    target_met = (
        summary["pass_rate"] == 1.0
        and summary["json_valid_rate"] == 1.0
        and summary["argument_accuracy_rate"] == 1.0
        and summary["empty_think_prefix_cases"] == 0
        and summary["residual_strict_failure_count"] == 0
        and len(changes) == 1
    )
    return {
        "run_id": summary["run_id"],
        "candidate": "qwen3-4b-strict-toolcall-v9-full140-runtime-profile-refusal-marker-normalized",
        "base_candidate": raw_report["candidate"],
        "status": "runtime-normalized-target-met" if target_met else "failed-gate-next-repair-needed",
        "target_met": target_met,
        "promotion_boundary": (
            "Runtime proof only. This does not publish or promote new v9/v10 weights; it proves the "
            "single residual text-mode forbidden marker can be removed at the runtime boundary while "
            "preserving the v9 tool-call passes."
        ),
        "normalizer": "text-refusal-forbidden-marker-redaction-v1",
        "raw_source_report": str(raw_report_path),
        "normalized_input_responses": str(normalized_input_path),
        "normalized_changes_json": str(changes_path),
        "summary_json": str(normalized_summary_path),
        "results_jsonl": str(normalized_summary_path.with_name("results.jsonl")),
        "responses_jsonl": str(normalized_input_path),
        "raw_v9": {
            "pass_rate": raw["pass_rate"],
            "json_valid_rate": raw["json_valid_rate"],
            "argument_accuracy_rate": raw["argument_accuracy_rate"],
            "empty_think_prefix_cases": raw["empty_think_prefix_cases"],
            "residual_strict_failure_count": raw["residual_strict_failure_count"],
            "residual_strict_failure_ids": raw["residual_strict_failure_ids"],
            "refusal_marker_echo_count": raw["refusal_marker_echo_count"],
        },
        "runtime_normalized": {
            "pass_rate": summary["pass_rate"],
            "json_valid_rate": summary["json_valid_rate"],
            "argument_accuracy_rate": summary["argument_accuracy_rate"],
            "empty_think_prefix_cases": summary["empty_think_prefix_cases"],
            "residual_strict_failure_count": summary["residual_strict_failure_count"],
            "residual_strict_failure_ids": summary["residual_strict_failure_ids"],
            "invalid_tool_handling_rate": summary["invalid_tool_handling_rate"],
            "multi_turn_repair_rate": summary["multi_turn_repair_rate"],
            "changed_response_count": len(changes),
            "changed_responses": changes,
        },
        "gate_decision": {
            "strict_pass_rate_target": 1.0,
            "json_valid_rate_target": 1.0,
            "argument_accuracy_rate_target": 1.0,
            "empty_think_prefix_target": 0,
            "residual_strict_failure_target": 0,
            "passed": target_met,
        },
        "next_action": (
            "Use this normalizer as the runtime-side safety/refusal unblock for v9 while leaving v10 "
            "marked failed. Any public model-weight claim remains blocked until a raw model run reaches "
            "the same gate without response normalization."
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    raw = report["raw_v9"]
    normalized = report["runtime_normalized"]
    lines = [
        "# Qwen3 v9 Runtime Refusal-Marker Normalization Proof",
        "",
        f"Run ID: `{report['run_id']}`",
        f"Status: `{report['status']}`",
        f"Target met: `{str(report['target_met']).lower()}`",
        f"Normalizer: `{report['normalizer']}`",
        "",
        report["promotion_boundary"],
        "",
        "## Gate Result",
        "",
        "| Metric | Raw v9 | Runtime-normalized v9 | Target |",
        "|---|---:|---:|---:|",
        f"| Strict pass rate | {raw['pass_rate']:.3f} | {normalized['pass_rate']:.3f} | 1.000 |",
        f"| JSON validity | {raw['json_valid_rate']:.3f} | {normalized['json_valid_rate']:.3f} | 1.000 |",
        f"| Argument accuracy | {raw['argument_accuracy_rate']:.3f} | {normalized['argument_accuracy_rate']:.3f} | 1.000 |",
        f"| Empty-think prefix cases | {raw['empty_think_prefix_cases']} | {normalized['empty_think_prefix_cases']} | 0 |",
        f"| Residual strict failures | {raw['residual_strict_failure_count']} | {normalized['residual_strict_failure_count']} | 0 |",
        f"| Changed text responses | 0 | {normalized['changed_response_count']} | 1 |",
        "",
        "## Changed Responses",
        "",
        f"- `{', '.join(item['id'] for item in normalized['changed_responses'])}`",
        "",
        "## Artifacts",
        "",
        f"- Raw source report: `{report['raw_source_report']}`",
        f"- Normalized input responses: `{report['normalized_input_responses']}`",
        f"- Changes JSON: `{report['normalized_changes_json']}`",
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
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()
    report = build_report()
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(f"wrote {args.json_output}")
    print(f"wrote {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
