#!/usr/bin/env python3
"""Validate the Qwen3 v4 official coding failure-analysis report."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-coding-failure-analysis-20260624.json"
REPORT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-coding-failure-analysis-20260624.md"


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
    if int(scores.get("task_count", 0)) != 164:
        failures.append("task count must be 164")
    if int(scores.get("base_pass_count", 0)) != 85:
        failures.append("base pass count must be 85")
    if int(scores.get("plus_pass_count", 0)) != 80:
        failures.append("plus pass count must be 80")
    if abs(float(scores.get("humaneval_base_pass_at_1", -1.0)) - 0.5182926829268293) > 1e-12:
        failures.append("base pass rate must match EvalPlus JSON")
    if abs(float(scores.get("humaneval_plus_pass_at_1", -1.0)) - 0.4878048780487805) > 1e-12:
        failures.append("plus pass rate must match EvalPlus JSON")

    status_counts = data.get("status_counts", {})
    expected_status = {"pass_both": 79, "base_fail": 79, "plus_only_fail": 6}
    for key, expected in expected_status.items():
        if int(status_counts.get(key, -1)) != expected:
            failures.append(f"status_counts.{key} must be {expected}")

    categories = data.get("failure_categories", {})
    expected_categories = {
        "empty_completion": 23,
        "syntax_or_pre_test_failure": 13,
        "likely_truncated_or_runaway": 12,
        "edge_case_generalization": 6,
        "missing_return": 14,
    }
    for key, expected in expected_categories.items():
        category = categories.get(key, {})
        if int(category.get("count", -1)) != expected:
            failures.append(f"failure_categories.{key}.count must be {expected}")
        task_ids = category.get("task_ids")
        if not isinstance(task_ids, list) or len(task_ids) < min(expected, 6):
            failures.append(f"failure_categories.{key}.task_ids must list affected tasks")

    decision = data.get("repair_decision", {})
    if decision.get("targeted_coding_repair_worthwhile") is not True:
        failures.append("targeted coding repair must be marked worthwhile")
    if decision.get("fine_tune_immediately") is not False:
        failures.append("fine_tune_immediately must remain false")
    if "generation/protocol failures" not in str(decision.get("reason", "")):
        failures.append("repair reason must identify generation/protocol failures")
    if "diagnostic" not in str(decision.get("claim_boundary", "")).lower():
        failures.append("claim boundary must keep analysis diagnostic")

    md = REPORT_MD.read_text(encoding="utf-8")
    for needle in (
        "Targeted coding repair is worthwhile",
        "do not start with broad fine-tuning",
        "HumanEval pass@1 `0.518`",
    ):
        if needle not in md:
            failures.append(f"markdown report missing {needle!r}")
    return finish(failures)


def finish(failures: list[str]) -> int:
    if failures:
        print("not ready: official coding failure analysis")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: official coding failure analysis")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
