#!/usr/bin/env python3
"""Validate the Qwen3 v12 BFCL parallel-call repair dataset and config."""
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
DATA_DIR = ROOT / "gemma4/data/strict_tool_call/expanded_splits_v12_bfcl_parallel_repair"
BASE_DIR = ROOT / "gemma4/data/strict_tool_call/expanded_splits_v11_bfcl_selected_repair"
MATERIALIZER = ROOT / "gemma4/data/strict_tool_call/tools/materialize_bfcl_parallel_repair_splits_v12.py"
CONFIG = ROOT / "gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v12-bfcl-parallel-repair.yaml"
REPAIR_PREFIX = "bfcl-v12-parallel-"
REQUIRED_REPAIR_ROWS = 10
REQUIRED_CATEGORY_COUNTS = {"bfcl_selected_parallel_v12": 10}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def assistant_target(row: dict) -> str:
    assistants = [msg for msg in row.get("messages", []) if msg.get("role") == "assistant"]
    if not assistants:
        return ""
    return str(assistants[-1].get("content", ""))


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
    if len(train) != len(base_train) + REQUIRED_REPAIR_ROWS:
        failures.append(f"v12 train must equal v11 train plus {REQUIRED_REPAIR_ROWS} parallel rows")
    if len(repair_rows) != REQUIRED_REPAIR_ROWS:
        failures.append(f"v12 repair row count must be {REQUIRED_REPAIR_ROWS}, got {len(repair_rows)}")
    category_counts = Counter(str(row.get("category", "")) for row in repair_rows)
    if dict(category_counts) != REQUIRED_CATEGORY_COUNTS:
        failures.append(f"v12 BFCL category counts must be {REQUIRED_CATEGORY_COUNTS}, got {dict(category_counts)}")

    ids = [str(row.get("id", "")) for row in train]
    if len(ids) != len(set(ids)):
        failures.append("v12 train ids must be unique")
    base_ids = {str(row.get("id", "")) for row in base_train}
    overlap = sorted(base_ids & {str(row.get("id", "")) for row in repair_rows})
    if overlap:
        failures.append(f"v12 BFCL repair ids must not overlap base rows: {overlap[:5]}")

    for row in repair_rows:
        row_id = row.get("id")
        messages = row.get("messages", [])
        if len(messages) != 3:
            failures.append(f"{row_id}: repair rows must be system/user/assistant only")
            continue
        system = str(messages[0].get("content", ""))
        target = assistant_target(row)
        if "Do not collapse parallel actions into a single call" not in system:
            failures.append(f"{row_id}: system prompt must include the v12 parallel anti-collapse instruction")
        if "<tools>" not in system or "</tools>" not in system:
            failures.append(f"{row_id}: system prompt must include tools")
        if "<think>" in target or "</think>" in target:
            failures.append(f"{row_id}: assistant target must not include thinking tags")
        if "```" in target:
            failures.append(f"{row_id}: assistant target must not include markdown fences")
        if target.count("<tool_call>") != target.count("</tool_call>"):
            failures.append(f"{row_id}: assistant target must contain balanced tool_call tags")
        if target.count("<tool_call>") < 2:
            failures.append(f"{row_id}: parallel repair target must contain at least two tool calls")
        if not target.strip().startswith("<tool_call>") or not target.strip().endswith("</tool_call>"):
            failures.append(f"{row_id}: assistant target must be only tool_call XML")
        for chunk in target.split("<tool_call>")[1:]:
            payload = chunk.split("</tool_call>", 1)[0].strip()
            try:
                decoded = json.loads(payload)
            except json.JSONDecodeError as exc:
                failures.append(f"{row_id}: tool-call payload is not JSON: {exc}")
                continue
            if sorted(decoded) != ["arguments", "name"]:
                failures.append(f"{row_id}: tool-call payload must contain only name and arguments")
            if not isinstance(decoded.get("arguments"), dict):
                failures.append(f"{row_id}: tool-call arguments must be an object")

    for split in ("val", "valid", "test"):
        rows = load_jsonl(data_dir / f"{split}.jsonl")
        if any(str(row.get("id", "")).startswith(REPAIR_PREFIX) for row in rows):
            failures.append(f"{split}.jsonl must not include v12 repair rows")
    if (data_dir / "val.jsonl").read_text(encoding="utf-8") != (data_dir / "valid.jsonl").read_text(encoding="utf-8"):
        failures.append("valid.jsonl must be an exact alias of val.jsonl")
    return failures


def validate_config() -> list[str]:
    failures: list[str] = []
    if not CONFIG.exists():
        return [f"missing {CONFIG.relative_to(ROOT)}"]
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    if cfg.get("model") != "Qwen/Qwen3-4B-MLX-4bit":
        failures.append("v12 config must keep the Qwen3 4B MLX base")
    if cfg.get("data") != "data/strict_tool_call/expanded_splits_v12_bfcl_parallel_repair":
        failures.append("v12 config must point at the v12 BFCL parallel repair dataset")
    if cfg.get("adapter_path") != "experiments/qwen3-4b-strict-toolcall-v12-bfcl-parallel-repair/lora_adapter":
        failures.append("v12 config must write to the v12 adapter path")
    if "v11" in str(cfg.get("adapter_path", "")):
        failures.append("v12 config must not overwrite v11 adapter artifacts")
    if int(cfg.get("iters", 0)) != 80:
        failures.append("v12 config should use the bounded 80-iteration parallel repair envelope")
    if float(cfg.get("learning_rate", 0.0)) > 1.0e-5:
        failures.append("v12 config should use a conservative repair learning rate")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-regeneration-check", action="store_true")
    args = parser.parse_args()
    failures = validate_dataset() + validate_config()
    if not args.skip_regeneration_check and not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_data = Path(tmp) / "expanded_splits_v12_bfcl_parallel_repair"
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
                if expected.read_text(encoding="utf-8") != actual.read_text(encoding="utf-8"):
                    failures.append(f"{actual.relative_to(ROOT)} is stale; regenerate it")
    if failures:
        print("not ready: qwen3 v12 BFCL parallel repair dataset")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: qwen3 v12 BFCL parallel repair dataset")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
