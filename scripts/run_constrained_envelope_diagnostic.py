#!/usr/bin/env python3
"""Replay pilot responses through a constrained runtime envelope diagnostic."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_endpoint_pilot_benchmark import score_case as score_pilot_case
from run_tool_call_benchmark import extract_tool_calls, save_jsonl
from run_tool_call_benchmark import score_case as score_tool_call_case


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = Path(os.environ.get("HERMES_EVAL_ROOT", "/Volumes/PortableSSD/hermes-evals"))
THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_number}: expected JSON object")
        rows.append(row)
    return rows


def render_tool_calls(calls: list[dict[str, Any]]) -> str:
    return "".join(
        f"<tool_call>{json.dumps(call, separators=(',', ':'), ensure_ascii=False)}</tool_call>"
        for call in calls
    )


def strip_thinking(text: str) -> str:
    return THINK_RE.sub("", text).strip()


def split_candidate_sentences(text: str) -> list[str]:
    compact = re.sub(r"\s+", " ", strip_thinking(text)).strip()
    if not compact:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", compact)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def expected_contains_any(expected: dict[str, Any]) -> list[str]:
    return [str(item).lower() for item in expected.get("contains_any", expected.get("must_contain_any", []))]


def expected_excludes_any(expected: dict[str, Any]) -> list[str]:
    return [str(item).lower() for item in expected.get("excludes_any", expected.get("must_not_contain_any", []))]


def constrain_refusal_text(response: str, expected: dict[str, Any]) -> tuple[str, str]:
    contains_any = expected_contains_any(expected)
    excludes_any = expected_excludes_any(expected)
    for sentence in split_candidate_sentences(response):
        lowered = sentence.lower()
        contains_ok = not contains_any or any(marker in lowered for marker in contains_any)
        excludes_ok = all(marker not in lowered for marker in excludes_any)
        if contains_ok and excludes_ok:
            return sentence, "selected-refusal-sentence"
    return strip_thinking(response), "stripped-thinking-only"


def apply_envelope(case: dict[str, Any], response: str) -> tuple[str, str]:
    expected = case.get("expected", {})
    if isinstance(expected, dict) and expected.get("mode") == "tool_calls":
        calls, errors, _leftover = extract_tool_calls(response)
        if calls and not errors:
            return render_tool_calls(calls), "selected-tool-calls"
        return strip_thinking(response), "stripped-thinking-only"
    if case.get("category") == "tool_call_exact":
        calls, errors, _leftover = extract_tool_calls(response)
        if calls and not errors:
            return render_tool_calls(calls), "selected-tool-calls"
        return strip_thinking(response), "stripped-thinking-only"
    if isinstance(expected, dict) and expected.get("mode") == "text":
        return constrain_refusal_text(response, expected)
    if case.get("category") == "contains_excludes":
        return constrain_refusal_text(response, expected if isinstance(expected, dict) else {})
    return strip_thinking(response), "stripped-thinking-only"


def scorer_for_suite(suite: list[dict[str, Any]]) -> str:
    categories = {str(case.get("category", "")) for case in suite}
    if categories <= {"tool_call_exact", "contains_excludes", "json_exact", "line_count", "code_contains"}:
        return "pilot"
    return "tool-call-heldout"


def score_enveloped_case(case: dict[str, Any], response: str, require_no_extra_tool_text: bool) -> dict[str, Any]:
    if scorer_for_suite([case]) == "pilot":
        return score_pilot_case(case, response, require_no_extra_tool_text)
    return score_tool_call_case(case, response)


def render_summary(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    by_category = Counter(row["category"] for row in rows)
    passed_by_category = Counter(row["category"] for row in rows if row["pass"])
    lines = [
        "# Constrained Envelope Diagnostic Summary",
        "",
        f"- Run id: `{summary['run_id']}`",
        f"- Model: `{summary['model']}`",
        f"- Suite: `{summary['suite']}`",
        f"- Source output: `{summary['source_output_dir']}`",
        f"- Raw pass rate: `{summary['raw_pass_rate']:.3f}`",
        f"- Constrained pass rate: `{summary['pass_rate']:.3f}`",
        "- Promotion allowed: `False`",
        "",
        "This is runtime-wrapper diagnostic evidence only. It does not promote raw model output.",
        "",
        "## Category Breakdown",
        "",
        "| Category | Cases | Pass rate |",
        "|---|---:|---:|",
    ]
    for category in sorted(by_category):
        lines.append(
            f"| {category} | {by_category[category]} | {passed_by_category[category] / by_category[category]:.3f} |"
        )
    lines.extend(["", "## Cases", "", "| Case | Envelope action | Pass | Reason |", "|---|---|---:|---|"])
    for row in rows:
        lines.append(
            f"| `{row['id']}` | `{row['envelope_action']}` | `{row['pass']}` | {row.get('reason', '')} |"
        )
    return "\n".join(lines) + "\n"


def compact_report(summary: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": summary["run_id"],
        "created_at": summary["created_at"],
        "model": summary["model"],
        "suite": summary["suite"],
        "source_output_dir": summary["source_output_dir"],
        "source_summary": summary["source_summary"],
        "output_dir": summary["output_dir"],
        "cases": summary["cases"],
        "raw_passed": summary["raw_passed"],
        "raw_pass_rate": summary["raw_pass_rate"],
        "constrained_passed": summary["passed"],
        "constrained_pass_rate": summary["pass_rate"],
        "promotion_allowed": False,
        "claim_boundary": (
            "Diagnostic envelope evidence is not raw-output promotion. Promotion requires a real runtime-wrapper "
            "gate with held-out BFCL, endpoint/local pilot, official benchmark, latency, rollback, and publication evidence."
        ),
        "case_results": [
            {
                "id": row["id"],
                "category": row["category"],
                "envelope_action": row["envelope_action"],
                "pass": row["pass"],
                "reason": row.get("reason", ""),
            }
            for row in rows
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--source-output-dir", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--run-id", default=f"constrained-envelope-diagnostic-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--report-json", type=Path)
    parser.add_argument("--report-md", type=Path)
    parser.add_argument("--require-no-extra-tool-text", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = load_json(args.suite)
    if not isinstance(suite, list) or not suite:
        raise ValueError("suite must be a non-empty JSON array")
    responses_path = args.source_output_dir / "responses.jsonl"
    source_summary_path = args.source_output_dir / "summary.json"
    raw_summary = load_json(source_summary_path)
    responses = {row["id"]: row for row in load_jsonl(responses_path)}
    output_dir = args.output_dir or DEFAULT_OUTPUT_ROOT / "standard-benchmarks" / "constrained-envelope" / args.run_id

    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"source_output_dir: {args.source_output_dir}")
        print(f"model: {args.model}")
        print(f"run_id: {args.run_id}")
        print(f"output_dir: {output_dir}")
        print(f"require_no_extra_tool_text: {args.require_no_extra_tool_text}")
        return 0

    rows: list[dict[str, Any]] = []
    output_responses: list[dict[str, Any]] = []
    for case in suite:
        case_id = case["id"]
        if case_id not in responses:
            raise ValueError(f"missing response for suite case {case_id}")
        response = str(responses[case_id].get("response", ""))
        constrained_response, action = apply_envelope(case, response)
        scored = score_enveloped_case(case, constrained_response, args.require_no_extra_tool_text)
        rows.append(
            {
                "id": case_id,
                "category": case["category"],
                "response": response,
                "constrained_response": constrained_response,
                "envelope_action": action,
                **scored,
            }
        )
        output_responses.append(
            {
                "id": case_id,
                "response": response,
                "constrained_response": constrained_response,
                "envelope_action": action,
            }
        )

    passed = sum(1 for row in rows if row["pass"])
    raw_passed = int(raw_summary.get("passed", 0))
    raw_cases = int(raw_summary.get("cases", len(rows)))
    summary = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "suite": str(args.suite),
        "model": args.model,
        "source_output_dir": str(args.source_output_dir),
        "source_summary": str(source_summary_path),
        "output_dir": str(output_dir),
        "require_no_extra_tool_text": args.require_no_extra_tool_text,
        "cases": len(rows),
        "passed": passed,
        "pass_rate": passed / len(rows),
        "raw_passed": raw_passed,
        "raw_pass_rate": raw_passed / raw_cases,
        "promotion_allowed": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    save_jsonl(output_dir / "responses.jsonl", output_responses)
    save_jsonl(output_dir / "results.jsonl", rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_summary(summary, rows), encoding="utf-8")
    report = compact_report(summary, rows)
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.report_md:
        args.report_md.parent.mkdir(parents=True, exist_ok=True)
        args.report_md.write_text(render_summary(summary, rows), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
