#!/usr/bin/env python3
"""Validate runtime prompt profile contracts."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "RUNTIME_PROMPT_PROFILES.yaml"
REQUIRED_PROFILE_KEYS = {
    "id",
    "model_family",
    "applies_to",
    "user_prefix",
    "assistant_prefill",
    "endpoint_strategy",
    "required_for",
    "evidence",
    "strict_result",
    "limitations",
}


def load_profiles(path: Path = PROFILE_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def validate_profiles(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    profiles = data.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        return ["profiles must be a non-empty list"]

    seen: set[str] = set()
    for index, profile in enumerate(profiles, 1):
        label = f"profile {index}"
        if not isinstance(profile, dict):
            errors.append(f"{label}: must be a mapping")
            continue
        missing = REQUIRED_PROFILE_KEYS - set(profile)
        if missing:
            errors.append(f"{label}: missing keys {sorted(missing)}")
            continue
        profile_id = profile["id"]
        label = str(profile_id)
        if not isinstance(profile_id, str) or not profile_id:
            errors.append(f"profile {index}: id must be a non-empty string")
        elif profile_id in seen:
            errors.append(f"{label}: duplicate id")
        else:
            seen.add(profile_id)

        for key in ("applies_to", "required_for", "limitations"):
            value = profile.get(key)
            if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
                errors.append(f"{label}: {key} must be a non-empty list of strings")

        if not isinstance(profile.get("user_prefix"), str):
            errors.append(f"{label}: user_prefix must be a string")
        if not isinstance(profile.get("assistant_prefill"), str):
            errors.append(f"{label}: assistant_prefill must be a string")
        if not isinstance(profile.get("endpoint_strategy"), str) or not profile["endpoint_strategy"]:
            errors.append(f"{label}: endpoint_strategy must be a non-empty string")

        evidence = profile.get("evidence")
        if not isinstance(evidence, dict) or not evidence:
            errors.append(f"{label}: evidence must be a non-empty mapping")
        else:
            for evidence_key, evidence_value in evidence.items():
                if not isinstance(evidence_key, str) or not isinstance(evidence_value, str) or not evidence_value:
                    errors.append(f"{label}: evidence entries must be string-to-string")

        strict_result = profile.get("strict_result")
        if not isinstance(strict_result, dict) or not strict_result:
            errors.append(f"{label}: strict_result must be a non-empty mapping")
        else:
            for metric, value in strict_result.items():
                if not isinstance(metric, str) or not isinstance(value, (int, float)):
                    errors.append(f"{label}: strict_result entries must be numeric")
                elif not 0 <= float(value) <= 1:
                    errors.append(f"{label}: strict_result {metric} must be in [0, 1]")
    return errors


def main() -> int:
    try:
        data = load_profiles()
        errors = validate_profiles(data)
    except Exception as exc:  # noqa: BLE001
        print(f"runtime prompt profiles invalid: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"ok: {PROFILE_PATH.name} ({len(data['profiles'])} profiles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
