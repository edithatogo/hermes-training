#!/usr/bin/env python3
"""Validate the Qwen3 v9 runtime safety/refusal profile selection report."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = (
    ROOT
    / "reports/benchmark/official-candidates/qwen3-v9-runtime-safety-refusal-profile-selection-20260624.json"
)
REPORT_MD = (
    ROOT
    / "reports/benchmark/official-candidates/qwen3-v9-runtime-safety-refusal-profile-selection-20260624.md"
)
PROFILE_CONTRACT = ROOT / "RUNTIME_PROMPT_PROFILES.yaml"


def main() -> int:
    failures: list[str] = []
    for path in (REPORT_JSON, REPORT_MD, PROFILE_CONTRACT):
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        return finish(failures)

    data = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
    if data.get("selected_profile") != "qwen3-v9-no-think-prefill-refusal-marker-normalized":
        failures.append("selected profile is not the v9 runtime-normalized profile")
    if data.get("status") != "runtime-profile-selected":
        failures.append("status must be runtime-profile-selected")

    metrics = data.get("metrics", {})
    raw_v9 = metrics.get("raw_v9", {})
    normalized = metrics.get("runtime_normalized_v9", {})
    raw_v10 = metrics.get("raw_v10", {})
    if float(raw_v9.get("strict_pass_rate", -1.0)) != 0.875:
        failures.append("raw v9 strict pass must remain 0.875")
    if float(normalized.get("strict_pass_rate", -1.0)) != 1.0:
        failures.append("runtime-normalized v9 strict pass must be 1.000")
    if float(normalized.get("json_valid_rate", -1.0)) != 1.0:
        failures.append("runtime-normalized v9 JSON validity must be 1.000")
    if float(normalized.get("argument_accuracy_rate", -1.0)) != 1.0:
        failures.append("runtime-normalized v9 argument accuracy must be 1.000")
    if int(normalized.get("residual_strict_failure_count", -1)) != 0:
        failures.append("runtime-normalized v9 residual failures must be 0")
    if int(normalized.get("changed_response_count", -1)) != 1:
        failures.append("runtime-normalized v9 changed response count must be 1")
    if float(raw_v10.get("strict_pass_rate", -1.0)) != 0.75:
        failures.append("raw v10 strict pass must remain 0.750")

    boundary = data.get("claim_boundary", {})
    if boundary.get("hermes_runtime_profile_selectable") is not True:
        failures.append("Hermes runtime profile must be selectable")
    for key in ("public_raw_model_weight_claim", "publish_v9_weights", "publish_v10_weights"):
        if boundary.get(key) is not False:
            failures.append(f"{key} must remain false")
    if "runtime response normalization" not in str(boundary.get("reason", "")):
        failures.append("claim boundary must explain runtime normalization dependency")

    md_text = REPORT_MD.read_text(encoding="utf-8")
    required_md = [
        "This is a runtime-profile selection, not a raw model-weight claim.",
        "v9 runtime-normalized profile",
        "Do not publish v9 or v10 weights",
    ]
    for needle in required_md:
        if needle not in md_text:
            failures.append(f"markdown report missing {needle!r}")

    profile_text = PROFILE_CONTRACT.read_text(encoding="utf-8")
    if str(data["selected_profile"]) not in profile_text:
        failures.append("runtime profile contract does not include selected profile")
    if "text-refusal-forbidden-marker-redaction-v1" not in profile_text:
        failures.append("runtime profile contract must name the marker normalizer")

    return finish(failures)


def finish(failures: list[str]) -> int:
    if failures:
        print("not ready: qwen3 v9 runtime safety profile selection")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: qwen3 v9 runtime safety profile selection")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
