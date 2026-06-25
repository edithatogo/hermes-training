#!/usr/bin/env python3
"""Validate the Qwen3 v11 BFCL completion-reasoning bridge report."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = (
    ROOT
    / "reports/benchmark/official-candidates/qwen3-v11-bfcl-completion-reasoning-bridge-30-20260625.json"
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
    if data.get("status") != "proxy-implemented-output-unchanged":
        failures.append("status must record unchanged output after proxy repair")
    if data.get("unchanged_from_v11_bridge") is not True:
        failures.append("report must state the result is unchanged from the v11 bridge")
    decision = data.get("decision", {})
    if decision.get("target_met") is not False:
        failures.append("target must remain unmet")
    if decision.get("bfcl_claim_allowed") is not False:
        failures.append("BFCL claim must remain blocked")
    if "BFCL OpenAI handler" not in str(decision.get("next_action", "")):
        failures.append("next action must move below the proxy into BFCL handler instrumentation")

    implementation = data.get("implementation", {})
    if implementation.get("flag") != "--completion-reasoning-tool-call-text":
        failures.append("implementation flag must be --completion-reasoning-tool-call-text")
    if implementation.get("script") != "scripts/openai_normalizing_proxy.py":
        failures.append("implementation script must be scripts/openai_normalizing_proxy.py")

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

    audit = data.get("row_audit", {})
    if int(audit.get("multiple", {}).get("visible_tool", -1)) != 0:
        failures.append("multiple visible_tool must remain 0 for this failed bridge")
    if int(audit.get("parallel", {}).get("decoded_one_call_invalid", -1)) != 3:
        failures.append("parallel decoded_one_call_invalid must remain 3")

    for key, value in data.get("artifacts", {}).items():
        path = Path(str(value))
        if key in {"generate_log", "evaluate_log", "overall_csv", "non_live_csv"} and not path.exists():
            failures.append(f"artifact missing: {value}")

    md = REPORT_MD.read_text(encoding="utf-8")
    for needle in (
        "proxy-implemented-output-unchanged",
        "--completion-reasoning-tool-call-text",
        "unchanged from the prior v11",
        "below the normalizing proxy",
    ):
        if needle not in md:
            failures.append(f"markdown report missing {needle!r}")
    return finish(failures)


def finish(failures: list[str]) -> int:
    if failures:
        print("not ready: qwen3 v11 BFCL completion-reasoning bridge report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: qwen3 v11 BFCL completion-reasoning bridge report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
