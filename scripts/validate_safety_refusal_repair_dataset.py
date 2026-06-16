#!/usr/bin/env python3
"""Validate the Qwen3 v4 safety/refusal repair dataset and config."""
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
DATA_DIR = ROOT / "gemma4/data/strict_tool_call/expanded_splits_v7_safety_refusal_repair"
BASE_DIR = ROOT / "gemma4/data/strict_tool_call/expanded_splits_v6_free_text_copy"
MATERIALIZER = ROOT / "gemma4/data/strict_tool_call/tools/materialize_safety_refusal_repair_splits_v7.py"
CONFIG = ROOT / "gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v7-safety-refusal-repair.yaml"
REPAIR_PREFIX = "exp-safety-repair"
REQUIRED_LANES = {"strict-empty-think-wrapper-removal": 6, "refusal-forbidden-name-suppression": 8}


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
        failures.append("v7 train must equal v6 train plus the repair rows")
    lane_counts = Counter(str(row.get("repair_lane", "")) for row in repair_rows)
    if dict(lane_counts) != REQUIRED_LANES:
        failures.append(f"repair lane counts must be {REQUIRED_LANES}, got {dict(lane_counts)}")
    heldout_ids = {
        "heldout-json-validity-inventory",
        "heldout-argument-correctness-lab-order",
        "heldout-invalid-tool-handling-payroll",
        "heldout-invalid-tool-handling-security",
        "heldout-multi-turn-repair-purchase-order",
        "safety-refusal-delete-customer-record",
        "safety-refusal-exfiltrate-secret",
        "safety-refusal-disable-mfa",
    }
    ids = [str(row.get("id", "")) for row in train]
    overlap = sorted(heldout_ids & set(ids))
    if overlap:
        failures.append(f"v7 repair train must not include held-out ids: {overlap}")
    for row in repair_rows:
        assistants = [msg for msg in row.get("messages", []) if msg.get("role") == "assistant"]
        if not assistants:
            failures.append(f"{row.get('id')}: missing assistant target")
            continue
        for message in assistants:
            content = str(message.get("content", ""))
            if "<think>" in content or "</think>" in content:
                failures.append(f"{row.get('id')}: assistant target contains thinking tags")
        if row.get("repair_lane") == "refusal-forbidden-name-suppression":
            target = str(assistants[-1].get("content", ""))
            if "<tool_call>" in target:
                failures.append(f"{row.get('id')}: refusal target must not contain tool calls")
            for marker in row.get("forbidden_markers", []):
                if str(marker).lower() in target.lower():
                    failures.append(f"{row.get('id')}: refusal target echoes forbidden marker {marker}")
    if (data_dir / "val.jsonl").read_text(encoding="utf-8") != (data_dir / "valid.jsonl").read_text(encoding="utf-8"):
        failures.append("valid.jsonl must be an exact alias of val.jsonl")
    return failures


def validate_config() -> list[str]:
    failures: list[str] = []
    if not CONFIG.exists():
        return [f"missing {CONFIG.relative_to(ROOT)}"]
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    if cfg.get("model") != "Qwen/Qwen3-4B-MLX-4bit":
        failures.append("v7 config must keep the Qwen3 4B MLX base")
    if cfg.get("data") != "data/strict_tool_call/expanded_splits_v7_safety_refusal_repair":
        failures.append("v7 config must point at the v7 repair dataset")
    if cfg.get("adapter_path") != "experiments/qwen3-4b-strict-toolcall-v7-safety-refusal-repair/lora_adapter":
        failures.append("v7 config must write to the v7 adapter path")
    if int(cfg.get("iters", 0)) < 120:
        failures.append("v7 config should keep enough iterations for a bounded repair run")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-regeneration-check", action="store_true")
    args = parser.parse_args()
    failures = validate_dataset() + validate_config()
    if not args.skip_regeneration_check and not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_data = Path(tmp) / "expanded_splits_v7_safety_refusal_repair"
            subprocess.run(
                [sys.executable, str(MATERIALIZER), "--output-dir", str(tmp_data)],
                cwd=ROOT,
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
        print("not ready: safety/refusal repair dataset")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: safety/refusal repair dataset")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
