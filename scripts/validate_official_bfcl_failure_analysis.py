#!/usr/bin/env python3
"""Validate the Qwen3 v4 official BFCL failure-analysis report."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-bfcl-failure-analysis-20260625.json"
REPORT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-bfcl-failure-analysis-20260625.md"


def main() -> int:
    failures: list[str] = []
    for path in (REPORT_JSON, REPORT_MD):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        return finish(failures)

    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    if data.get("candidate") != "qwen3-4b-strict-toolcall-v4-targeted":
        failures.append("candidate must be qwen3-4b-strict-toolcall-v4-targeted")
    scores = data.get("scores", {})
    expected_scores = {
        "overall_acc": 0.0065,
        "non_live_overall_acc": 0.0646,
        "simple_python_ast": 0.265,
        "multiple_ast": 0.17,
        "parallel_ast": 0.0,
    }
    for key, expected in expected_scores.items():
        if abs(float(scores.get(key, -1.0)) - expected) > 1e-12:
            failures.append(f"scores.{key} must be {expected}")

    category = data.get("category_analysis", {})
    expected_categories = {
        "simple_python": {
            "rows": 400,
            "correct": 106,
            "invalid_rows": 294,
            "raw_blank_rows": 116,
            "raw_text_no_tool_call_rows": 171,
            "decoded_empty_rows": 287,
            "reasoning_tool_call_rows": 287,
        },
        "multiple": {
            "rows": 200,
            "correct": 34,
            "invalid_rows": 166,
            "raw_blank_rows": 92,
            "raw_text_no_tool_call_rows": 70,
            "decoded_empty_rows": 162,
            "reasoning_tool_call_rows": 162,
        },
        "parallel": {
            "rows": 200,
            "correct": 0,
            "invalid_rows": 200,
            "raw_blank_rows": 33,
            "raw_text_no_tool_call_rows": 106,
            "decoded_empty_rows": 139,
            "decoded_one_call_invalid_rows": 61,
            "reasoning_tool_call_rows": 139,
        },
    }
    for suite, expected_values in expected_categories.items():
        suite_data = category.get(suite, {})
        for key, expected in expected_values.items():
            if int(suite_data.get(key, -1)) != expected:
                failures.append(f"category_analysis.{suite}.{key} must be {expected}")

    taxonomy = data.get("failure_taxonomy", {})
    expected_taxonomy = {
        "final_answer_instead_of_tool_call": 347,
        "blank_final_result": 241,
        "hidden_reasoning_tool_call_not_scored": 588,
        "visible_wrong_call_count": 61,
        "visible_argument_or_value_error": 11,
    }
    for key, expected in expected_taxonomy.items():
        if int(taxonomy.get(key, {}).get("count", -1)) != expected:
            failures.append(f"failure_taxonomy.{key}.count must be {expected}")

    decision = data.get("repair_decision", {})
    if decision.get("targeted_repair_worthwhile") is not True:
        failures.append("targeted repair must be worthwhile")
    if decision.get("fine_tune_immediately") is not False:
        failures.append("fine_tune_immediately must remain false")
    if "runtime/proxy" not in str(decision.get("primary_repair_lane", "")):
        failures.append("primary repair lane must be runtime/proxy first")
    if "diagnostic" not in str(decision.get("claim_boundary", "")).lower():
        failures.append("claim boundary must keep report diagnostic")

    md = REPORT_MD.read_text(encoding="utf-8")
    for needle in (
        "Most failures decode as",
        "Targeted repair is worthwhile",
        "do not start with broad fine-tuning",
        "parallel `0.000`",
    ):
        if needle not in md:
            failures.append(f"markdown report missing {needle!r}")
    return finish(failures)


def finish(failures: list[str]) -> int:
    if failures:
        print("not ready: official BFCL failure analysis")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: official BFCL failure analysis")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
