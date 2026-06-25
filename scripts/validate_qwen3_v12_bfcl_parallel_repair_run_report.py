#!/usr/bin/env python3
"""Validate the Qwen3 v12 BFCL parallel repair run report."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = (
    ROOT
    / "reports/benchmark/official-candidates/qwen3-v12-bfcl-parallel-repair-30-20260626.json"
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
    if data.get("status") != "completed-no-promotion-parallel-single-call-collapse":
        failures.append("status must record completed-no-promotion parallel single-call collapse")
    decision = data.get("decision", {})
    if decision.get("target_met") is not False:
        failures.append("target must remain unmet")
    if decision.get("bfcl_claim_allowed") is not False:
        failures.append("BFCL claim must remain blocked")
    if "runtime continuation" not in str(decision.get("next_action", "")):
        failures.append("next action must move beyond the v12 10-row LoRA nudge")

    implementation = data.get("implementation", {})
    if implementation.get("repair_rows") != 10:
        failures.append("implementation must record 10 v12 repair rows")
    if implementation.get("materializer") != "gemma4/data/strict_tool_call/tools/materialize_bfcl_parallel_repair_splits_v12.py":
        failures.append("implementation must reference the v12 materializer")
    training = implementation.get("training", {})
    if int(training.get("iters", 0)) != 80:
        failures.append("training must record 80 iterations")
    if float(training.get("final_val_loss", 99.0)) > 1.0:
        failures.append("training final validation loss should be at or below 1.0")

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
    parallel = audit.get("parallel", {})
    if int(parallel.get("single_tool_block", -1)) != 10:
        failures.append("parallel single_tool_block must be 10")
    if int(parallel.get("multi_tool_block", -1)) != 0:
        failures.append("parallel multi_tool_block must be 0")
    if parallel.get("bfcl_error") != "Wrong number of functions.":
        failures.append("parallel BFCL error must be Wrong number of functions.")

    strict_gate = data.get("strict_gate", {})
    if strict_gate.get("allowed") is not False:
        failures.append("strict gate must remain fail-closed")
    if "exactly one tool call" not in str(strict_gate.get("reason", "")):
        failures.append("strict gate reason must cite single-call collapse")

    for key, value in data.get("artifacts", {}).items():
        path = Path(str(value))
        if key in {"adapter_config", "generate_log", "evaluate_log", "overall_csv", "non_live_csv", "training_log"} and not path.exists():
            failures.append(f"artifact missing: {value}")

    md = REPORT_MD.read_text(encoding="utf-8")
    for needle in (
        "completed-no-promotion-parallel-single-call-collapse",
        "Selected `parallel`: `0.00%`",
        "10/10 single tool blocks",
        "Wrong number of functions.",
        "runtime continuation",
    ):
        if needle not in md:
            failures.append(f"markdown report missing {needle!r}")
    return finish(failures)


def finish(failures: list[str]) -> int:
    if failures:
        print("not ready: qwen3 v12 BFCL parallel repair run report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: qwen3 v12 BFCL parallel repair run report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
