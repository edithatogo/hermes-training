#!/usr/bin/env python3
"""Validate the Qwen3 v9 residual refusal-marker repair dataset and config."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "gemma4/data/strict_tool_call/expanded_splits_v9_runtime_profile_refusal_marker_repair"
BASE_DIR = ROOT / "gemma4/data/strict_tool_call/expanded_splits_v8_wrapper_copy_refusal_repair"
MATERIALIZER = ROOT / "gemma4/data/strict_tool_call/tools/materialize_safety_refusal_repair_splits_v9.py"
CONFIG = ROOT / "gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v9-runtime-profile-refusal-marker-repair.yaml"
REPAIR_PREFIX = "exp-v9-"
REQUIRED_LANES = {"residual-refusal-marker-suppression": 4}
TARGET_RESIDUAL_IDS = {
    "heldout-invalid-tool-handling-payroll",
    "safety-refusal-delete-customer-record",
}
HELDOUT_IDS = {
    "heldout-json-validity-inventory",
    "heldout-argument-correctness-lab-order",
    "heldout-invalid-tool-handling-payroll",
    "heldout-invalid-tool-handling-security",
    "heldout-multi-turn-repair-purchase-order",
    "safety-refusal-delete-customer-record",
    "safety-refusal-exfiltrate-secret",
    "safety-refusal-disable-mfa",
}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def validate_dataset(data_dir: Path = DATA_DIR) -> list[str]:
    failures: list[str] = []
    for split in ("train", "val", "valid", "test"):
        path = data_dir / f"{split}.jsonl"
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")
    if failures:
        return failures

    train = load_jsonl(data_dir / "train.jsonl")
    base_train = load_jsonl(BASE_DIR / "train.jsonl")
    repair_rows = [row for row in train if str(row.get("id", "")).startswith(REPAIR_PREFIX)]
    if len(train) != len(base_train) + sum(REQUIRED_LANES.values()):
        failures.append("v9 train must equal v8 train plus the narrow v9 repair rows")
    lane_counts = Counter(str(row.get("repair_lane", "")) for row in repair_rows)
    if dict(lane_counts) != REQUIRED_LANES:
        failures.append(f"v9 repair lane counts must be {REQUIRED_LANES}, got {dict(lane_counts)}")
    overlap = sorted(HELDOUT_IDS & {str(row.get("id", "")) for row in train})
    if overlap:
        failures.append(f"v9 repair train must not include held-out ids: {overlap}")
    targeted = set()
    for row in repair_rows:
        targeted.update(str(item) for item in row.get("targets_residual_ids", []))
        assistants = [msg for msg in row.get("messages", []) if msg.get("role") == "assistant"]
        if not assistants:
            failures.append(f"{row.get('id')}: missing assistant target")
            continue
        final = str(assistants[-1].get("content", ""))
        if "<tool_call>" in final:
            failures.append(f"{row.get('id')}: refusal target must not contain tool calls")
        if "<think>" in final or "</think>" in final:
            failures.append(f"{row.get('id')}: refusal target must not contain thinking tags")
        if not any(marker in final.lower() for marker in ("cannot", "not available", "unable", "do not have")):
            failures.append(f"{row.get('id')}: refusal target must include a scorer refusal marker")
        for marker in row.get("forbidden_markers", []):
            if str(marker).lower() in final.lower():
                failures.append(f"{row.get('id')}: refusal target echoes forbidden marker {marker}")
    if targeted != TARGET_RESIDUAL_IDS:
        failures.append(f"v9 repair rows must target residual ids {sorted(TARGET_RESIDUAL_IDS)}, got {sorted(targeted)}")
    if (data_dir / "val.jsonl").read_text(encoding="utf-8") != (data_dir / "valid.jsonl").read_text(encoding="utf-8"):
        failures.append("valid.jsonl must be an exact alias of val.jsonl")
    return failures


def validate_config() -> list[str]:
    failures: list[str] = []
    if not CONFIG.exists():
        return [f"missing {CONFIG.relative_to(ROOT)}"]
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    if cfg.get("model") != "Qwen/Qwen3-4B-MLX-4bit":
        failures.append("v9 config must keep the Qwen3 4B MLX base")
    if cfg.get("data") != "data/strict_tool_call/expanded_splits_v9_runtime_profile_refusal_marker_repair":
        failures.append("v9 config must point at the v9 repair dataset")
    if cfg.get("adapter_path") != "experiments/qwen3-4b-strict-toolcall-v9-runtime-profile-refusal-marker-repair/lora_adapter":
        failures.append("v9 config must write to the v9 adapter path")
    if "v8" in str(cfg.get("adapter_path", "")):
        failures.append("v9 config must not overwrite v8 adapter artifacts")
    if int(cfg.get("iters", 0)) > 100:
        failures.append("v9 config should stay narrow and bounded")
    if float(cfg.get("learning_rate", 0.0)) > 2.0e-5:
        failures.append("v9 config should use a conservative repair learning rate")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-regeneration-check", action="store_true")
    args = parser.parse_args()
    failures = validate_dataset() + validate_config()
    if not args.skip_regeneration_check and not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_data = Path(tmp) / "expanded_splits_v9_runtime_profile_refusal_marker_repair"
            subprocess.run(
                [sys.executable, str(MATERIALIZER), "--output-dir", str(tmp_data)],
                cwd=ROOT / "gemma4/data/strict_tool_call/tools",
                check=True,
                capture_output=True,
                text=True,
            )
            for split in ("train", "val", "valid", "test"):
                expected = tmp_data / f"{split}.jsonl"
                actual = DATA_DIR / f"{split}.jsonl"
                if not expected.exists():
                    failures.append(f"materializer did not produce {split}.jsonl")
                    continue
                if expected.read_text(encoding="utf-8") != actual.read_text(encoding="utf-8"):
                    failures.append(f"{actual.relative_to(ROOT)} is stale; regenerate it")
    if failures:
        print("not ready: qwen3 v9 repair dataset")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: qwen3 v9 repair dataset")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
