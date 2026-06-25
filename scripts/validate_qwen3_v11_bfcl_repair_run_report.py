#!/usr/bin/env python3
"""Validate the Qwen3 v11 BFCL selected repair-run report."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v11-bfcl-selected-repair-run-20260625.json"
REPORT_MD = REPORT_JSON.with_suffix(".md")


def main() -> int:
    failures: list[str] = []
    for path in (REPORT_JSON, REPORT_MD):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        return finish(failures)

    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    if data.get("candidate") != "qwen3-4b-strict-toolcall-v11-bfcl-selected-repair":
        failures.append("candidate must be qwen3-4b-strict-toolcall-v11-bfcl-selected-repair")
    if data.get("status") != "trained-but-bfcl-bridge-regressed":
        failures.append("status must remain trained-but-bfcl-bridge-regressed")
    decision = data.get("decision", {})
    if decision.get("target_met") is not False:
        failures.append("target_met must be false")
    if decision.get("bfcl_claim_allowed") is not False:
        failures.append("BFCL claim must not be allowed")
    if decision.get("publication_allowed") is not False:
        failures.append("publication must not be allowed")
    if "Do not expand v11" not in str(decision.get("next_action", "")):
        failures.append("next action must block full selected-slice expansion")

    training = data.get("training_observation", {})
    expected_training = {
        "iters": 180,
        "train_samples": 820,
        "valid_samples": 5,
        "trained_tokens": 53898,
    }
    for key, expected in expected_training.items():
        if int(training.get(key, -1)) != expected:
            failures.append(f"training_observation.{key} must be {expected}")
    if abs(float(training.get("final_val_loss", -1.0)) - 0.791) > 1e-9:
        failures.append("final_val_loss must match the recorded run")
    if abs(float(training.get("peak_memory_gb", -1.0)) - 3.794) > 1e-9:
        failures.append("peak_memory_gb must match the recorded run")

    scores = data.get("scores", {})
    expected_scores = {
        "overall_acc": 0.0008,
        "non_live_overall_acc": 0.0083,
        "simple_python_ast": 0.1,
        "multiple_ast": 0.0,
        "parallel_ast": 0.0,
    }
    for key, expected in expected_scores.items():
        if abs(float(scores.get(key, -1.0)) - expected) > 1e-9:
            failures.append(f"scores.{key} must be {expected}")
    delta = data.get("delta_from_base_bridge", {})
    if float(delta.get("multiple_ast", 0.0)) >= 0.0:
        failures.append("multiple_ast delta must record the regression")
    if float(delta.get("parallel_ast", 1.0)) != 0.0:
        failures.append("parallel_ast delta must remain unchanged at 0")

    audit = data.get("row_audit", {})
    if int(audit.get("multiple", {}).get("visible_tool", -1)) != 0:
        failures.append("multiple visible_tool count must record 0")
    if int(audit.get("parallel", {}).get("decoded_one_call_invalid", -1)) != 3:
        failures.append("parallel decoded_one_call_invalid count must record 3")

    for key, value in data.get("artifacts", {}).items():
        path = ROOT / value if str(value).startswith("gemma4/") else Path(str(value))
        if key in {"training_log", "generate_log", "evaluate_log", "overall_csv", "non_live_csv"} and not path.exists():
            failures.append(f"artifact missing: {value}")

    md = REPORT_MD.read_text(encoding="utf-8")
    for needle in (
        "trained-but-bfcl-bridge-regressed",
        "Do not expand v11",
        "runtime/content-channel",
        "multiple` dropped from `10%` to `0%`",
    ):
        if needle not in md:
            failures.append(f"markdown report missing {needle!r}")
    return finish(failures)


def finish(failures: list[str]) -> int:
    if failures:
        print("not ready: qwen3 v11 BFCL repair-run report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: qwen3 v11 BFCL repair-run report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
