#!/usr/bin/env python3
"""Validate the runtime/training format ladder."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
LANES_PATH = ROOT / "RUNTIME_FORMAT_LANES.yaml"

REQUIRED_TOP_LEVEL = ("updated", "storage_root", "policy", "lanes")
REQUIRED_LANE_FIELDS = (
    "id",
    "kind",
    "primary_environment",
    "tools",
    "best_for",
    "artifact_formats",
    "proof_required",
    "not_for",
)
ALLOWED_ENVIRONMENTS = {
    "mac-mlx",
    "mac-ollama",
    "mac-lmstudio",
    "azure-cuda",
    "hf-transformers",
    "hosted-api",
    "retrieval",
    "specialist-runtime",
}


def expect_non_empty_list(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        errors.append(f"{label}: expected a non-empty list of strings")


def main() -> int:
    errors: list[str] = []
    data = yaml.safe_load(LANES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print(f"{LANES_PATH}: expected mapping", file=sys.stderr)
        return 1

    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            errors.append(f"missing top-level field: {field}")

    lanes = data.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        errors.append("lanes: expected a non-empty list")
        lanes = []

    seen_ids: set[str] = set()
    for index, lane in enumerate(lanes, 1):
        if not isinstance(lane, dict):
            errors.append(f"lanes[{index}]: expected mapping")
            continue
        lane_id = str(lane.get("id", f"<lane {index}>"))
        if lane_id in seen_ids:
            errors.append(f"{lane_id}: duplicate lane id")
        seen_ids.add(lane_id)
        for field in REQUIRED_LANE_FIELDS:
            if field not in lane:
                errors.append(f"{lane_id}: missing {field}")
        environment = lane.get("primary_environment")
        if environment not in ALLOWED_ENVIRONMENTS:
            errors.append(f"{lane_id}: invalid primary_environment {environment!r}")
        for field in ("tools", "best_for", "artifact_formats", "proof_required", "not_for"):
            expect_non_empty_list(lane.get(field), f"{lane_id}.{field}", errors)

    if "gguf-portability" not in seen_ids:
        errors.append("missing required GGUF portability lane")
    if "mlx-native" not in seen_ids:
        errors.append("missing required MLX native lane")
    if "unsloth-cloud" not in seen_ids:
        errors.append("missing required Unsloth cloud lane")

    if errors:
        for error in errors:
            print(f"format-lanes: {error}", file=sys.stderr)
        return 1

    print(f"ok: {LANES_PATH.name} ({len(lanes)} lanes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
