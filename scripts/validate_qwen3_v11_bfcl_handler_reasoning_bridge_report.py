#!/usr/bin/env python3
"""Validate the Qwen3 v11 BFCL handler reasoning bridge report."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = (
    ROOT
    / "reports/benchmark/official-candidates/qwen3-v11-bfcl-handler-reasoning-bridge-30-20260625.json"
)
REPORT_MD = REPORT_JSON.with_suffix(".md")


def main() -> int:
    failures: list[str] = []
    for path in (REPORT_JSON, REPORT_MD):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        return finish(failures)

    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    if data.get("status") != "handler-bridge-output-shape-fixed-parallel-still-blocked":
        failures.append("status must record handler output-shape fix with parallel still blocked")
    decision = data.get("decision", {})
    if decision.get("target_met") is not False:
        failures.append("target must remain unmet")
    if decision.get("bfcl_claim_allowed") is not False:
        failures.append("BFCL claim must remain blocked")
    if "v12 parallel-call repair" not in str(decision.get("next_action", "")):
        failures.append("next action must target v12 parallel-call repair")

    implementation = data.get("implementation", {})
    if implementation.get("local_bfcl_patch") != "scripts/patch_bfcl_qwen_reasoning_bridge.py":
        failures.append("implementation must reference the guarded local BFCL patch script")
    if implementation.get("patch_marker") != "HERMES_REASONING_TOOL_CALL_BRIDGE":
        failures.append("implementation must record the BFCL patch marker")

    scores = data.get("scores", {})
    expected_scores = {
        "overall_acc": 0.0333,
        "non_live_overall_acc": 0.3333,
        "simple_python_ast": 1.0,
        "multiple_ast": 1.0,
        "parallel_ast": 0.0,
    }
    for key, expected in expected_scores.items():
        if abs(float(scores.get(key, -1.0)) - expected) > 1e-9:
            failures.append(f"scores.{key} must be {expected}")

    audit = data.get("row_audit", {})
    for category in ("simple_python", "multiple", "parallel"):
        category_audit = audit.get(category, {})
        if int(category_audit.get("rows", -1)) != 10:
            failures.append(f"{category} rows must be 10")
        if int(category_audit.get("visible_tool", -1)) != 10:
            failures.append(f"{category} visible_tool must be 10")
        if int(category_audit.get("blank_result", -1)) != 0:
            failures.append(f"{category} blank_result must be 0")
        if int(category_audit.get("prose_no_tool", -1)) != 0:
            failures.append(f"{category} prose_no_tool must be 0")

    strict_gate = data.get("strict_gate", {})
    if strict_gate.get("allowed") is not False:
        failures.append("strict gate must remain fail-closed")
    if "parallel AST remains 0.00%" not in str(strict_gate.get("reason", "")):
        failures.append("strict gate reason must cite the parallel AST blocker")

    for key, value in data.get("artifacts", {}).items():
        path = Path(str(value))
        if key in {"generate_log", "evaluate_log", "overall_csv", "non_live_csv"} and not path.exists():
            failures.append(f"artifact missing: {value}")

    md = REPORT_MD.read_text(encoding="utf-8")
    for needle in (
        "handler-bridge-output-shape-fixed-parallel-still-blocked",
        "scripts/patch_bfcl_qwen_reasoning_bridge.py",
        "All 30 selected rows now contain visible `<tool_call>` blocks",
        "parallel cases still score `0.00%`",
    ):
        if needle not in md:
            failures.append(f"markdown report missing {needle!r}")
    return finish(failures)


def finish(failures: list[str]) -> int:
    if failures:
        print("not ready: qwen3 v11 BFCL handler reasoning bridge report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: qwen3 v11 BFCL handler reasoning bridge report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
