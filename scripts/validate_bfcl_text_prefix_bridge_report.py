#!/usr/bin/env python3
"""Validate the Qwen3 v4 BFCL text-prefix bridge smoke report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = (
    ROOT / "reports/benchmark/official-candidates/qwen3-v4-bfcl-text-prefix-bridge-30-20260625.json"
)
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-bfcl-text-prefix-bridge-30-20260625.md"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    failures: list[str] = []
    for path in (args.json_report, args.markdown_report):
        if not path.exists():
            failures.append(f"missing {display_path(path)}")
    if failures:
        print("not ready: BFCL text-prefix bridge report")
        for failure in failures:
            print(f"- {failure}")
        return 1

    data = json.loads(args.json_report.read_text(encoding="utf-8"))
    if data.get("status") != "scored-repair-evidence-fail-closed":
        failures.append("status must remain scored-repair-evidence-fail-closed")
    scores = data.get("scores", {})
    expected_scores = {
        "overall_acc": 0.0033,
        "non_live_overall_acc": 0.0333,
        "simple_python_ast": 0.1,
        "multiple_ast": 0.1,
        "parallel_ast": 0.0,
    }
    for key, expected in expected_scores.items():
        if abs(float(scores.get(key, -1.0)) - expected) > 0.0001:
            failures.append(f"{key} expected {expected}")
    if data.get("decision", {}).get("bfcl_claim_allowed") is not False:
        failures.append("BFCL claim must remain blocked")
    if data.get("decision", {}).get("runtime_bridge_helped") is not True:
        failures.append("runtime bridge should be recorded as helpful")
    if data.get("decision", {}).get("targeted_training_still_required") is not True:
        failures.append("targeted training should remain required")
    if "not a full BFCL leaderboard score" not in str(data.get("publication_boundary", "")):
        failures.append("publication boundary must block full BFCL claims")

    expected_audit = {
        "simple_python": {"rows": 10, "blank": 1, "visible_tool": 1, "reasoning_content": 9, "prose_no_tool": 8},
        "multiple": {"rows": 10, "blank": 4, "visible_tool": 1, "reasoning_content": 9, "prose_no_tool": 5},
        "parallel": {"rows": 10, "blank": 2, "visible_tool": 1, "reasoning_content": 9, "prose_no_tool": 7},
    }
    if data.get("row_audit") != expected_audit:
        failures.append("row audit changed unexpectedly")

    markdown = args.markdown_report.read_text(encoding="utf-8")
    for phrase in (
        "BFCL used `/v1/completions`",
        "chat `reasoning_content` promotion path was not exercised",
        "simple_python AST | 0.100",
        "multiple AST | 0.100",
        "parallel AST | 0.000",
        "not a passing Hermes tool-call claim",
    ):
        if phrase not in markdown:
            failures.append(f"markdown missing {phrase!r}")

    if failures:
        print("not ready: BFCL text-prefix bridge report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: BFCL text-prefix bridge report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
