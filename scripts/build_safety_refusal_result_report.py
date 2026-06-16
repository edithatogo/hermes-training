#!/usr/bin/env python3
"""Build a compact repo report for the Qwen3 v4 safety/refusal run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"
    "qwen3-v4-peft-safety-refusal-20260616/summary.json"
)
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-safety-refusal-result-20260616.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-safety-refusal-result-20260616.md"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def build_report(summary_path: Path = DEFAULT_SUMMARY) -> dict[str, Any]:
    summary = load_json(summary_path)
    output_dir = Path(str(summary["output_dir"]))
    return {
        "run_id": summary["run_id"],
        "suite": "safety-refusal",
        "candidate": "qwen3-4b-strict-toolcall-v4-targeted",
        "model": summary["model"],
        "adapter": summary["adapter"],
        "summary_json": str(summary_path),
        "results_jsonl": str(output_dir / "results.jsonl"),
        "responses_jsonl": str(output_dir / "responses.jsonl"),
        "status": "scored-repair-needed",
        "cases": summary["cases"],
        "passed": summary["passed"],
        "pass_rate": summary["pass_rate"],
        "json_valid_rate": summary["json_valid_rate"],
        "argument_accuracy_rate": summary["argument_accuracy_rate"],
        "empty_think_stripped_pass_rate": summary["empty_think_stripped_pass_rate"],
        "invalid_tool_handling_rate": summary["invalid_tool_handling_rate"],
        "multi_turn_repair_rate": summary["multi_turn_repair_rate"],
        "strict_failures_rescued_by_empty_think_strip": summary["strict_failures_rescued_by_empty_think_strip"],
        "strict_failures_rescued_by_empty_think_strip_ids": summary[
            "strict_failures_rescued_by_empty_think_strip_ids"
        ],
        "residual_strict_failure_count": summary["residual_strict_failure_count"],
        "residual_strict_failure_ids": summary["residual_strict_failure_ids"],
        "residual_strict_failure_reasons": summary["residual_strict_failure_reasons"],
        "publication_boundary": (
            "This is scored internal candidate evidence only. Do not claim standardized safety/refusal "
            "performance or public safety readiness from this suite."
        ),
        "next_action": (
            "Prioritize refusal repair: prevent unavailable/disallowed tool names from appearing in text "
            "responses and remove the empty-think wrapper from strict Hermes tool-call outputs."
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 v4 Safety/Refusal Result",
        "",
        f"Run ID: `{report['run_id']}`",
        f"Status: `{report['status']}`",
        f"Candidate: `{report['candidate']}`",
        f"Model: `{report['model']}`",
        f"Adapter: `{report['adapter']}`",
        "",
        report["publication_boundary"],
        "",
        "## Metrics",
        "",
        f"- Cases: `{report['cases']}`",
        f"- Passed: `{report['passed']}`",
        f"- Strict pass rate: `{report['pass_rate']:.3f}`",
        f"- JSON validity rate: `{report['json_valid_rate']:.3f}`",
        f"- Argument accuracy rate: `{report['argument_accuracy_rate']:.3f}`",
        f"- Empty-think stripped pass rate: `{report['empty_think_stripped_pass_rate']:.3f}`",
        f"- Invalid-tool handling rate: `{report['invalid_tool_handling_rate']:.3f}`",
        f"- Multi-turn repair rate: `{report['multi_turn_repair_rate']:.3f}`",
        "",
        "## Failure Focus",
        "",
        f"- Empty-think rescued IDs: `{', '.join(report['strict_failures_rescued_by_empty_think_strip_ids'])}`",
        f"- Residual strict failure IDs: `{', '.join(report['residual_strict_failure_ids'])}`",
        "",
        "## Artifacts",
        "",
        f"- Summary JSON: `{report['summary_json']}`",
        f"- Results JSONL: `{report['results_jsonl']}`",
        f"- Responses JSONL: `{report['responses_jsonl']}`",
        "",
        "## Next Action",
        "",
        report["next_action"],
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    report = build_report(args.summary)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"status": report["status"], "pass_rate": report["pass_rate"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
