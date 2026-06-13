#!/usr/bin/env python3
"""Validate Gemma 4 no-thinking training datasets and configs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

try:
    from materialize_gemma4_no_thinking_dataset import EMPTY_THOUGHT_CHANNEL
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.*
    from scripts.materialize_gemma4_no_thinking_dataset import EMPTY_THOUGHT_CHANNEL


ROOT = Path(__file__).resolve().parents[1]
GEMMA4_NO_THINKING_MODELS = {
    "google/gemma-4-26B-A4B-it",
    "google/gemma-4-31B-it",
}
SPLIT_NAMES = ("train", "val", "valid", "test")


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: config is not a YAML object")
    return data


def validate_dataset(data_dir: Path) -> list[str]:
    errors: list[str] = []
    found_split = False
    for split in SPLIT_NAMES:
        path = data_dir / f"{split}.jsonl"
        if not path.exists():
            continue
        found_split = True
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"{path}:{line_number}: invalid JSON: {exc}")
                    continue
                messages = record.get("messages") if isinstance(record, dict) else None
                if not isinstance(messages, list):
                    errors.append(f"{path}:{line_number}: missing messages list")
                    continue
                assistant_count = 0
                for index, message in enumerate(messages, 1):
                    if not isinstance(message, dict):
                        errors.append(f"{path}:{line_number}: message {index} is not an object")
                        continue
                    if message.get("role") != "assistant":
                        continue
                    assistant_count += 1
                    content = message.get("content")
                    if not isinstance(content, str):
                        errors.append(f"{path}:{line_number}: assistant message {index} content is not a string")
                    elif not content.startswith(EMPTY_THOUGHT_CHANNEL):
                        errors.append(
                            f"{path}:{line_number}: assistant message {index} is missing Gemma 4 empty thought channel"
                        )
                if assistant_count == 0:
                    errors.append(f"{path}:{line_number}: no assistant message found")
    if not found_split:
        errors.append(f"{data_dir}: no split JSONL files found")
    return errors


def validate_config(path: Path) -> list[str]:
    cfg = load_config(path)
    model = cfg.get("model")
    if model not in GEMMA4_NO_THINKING_MODELS:
        return []

    errors: list[str] = []
    if cfg.get("gemma4_no_thinking_empty_channel") is not True:
        errors.append(f"{path}: missing gemma4_no_thinking_empty_channel: true")

    data = cfg.get("data")
    if not isinstance(data, str):
        errors.append(f"{path}: missing data path")
        return errors
    data_dir = Path(data)
    if not data_dir.is_absolute():
        data_dir = path.parent.parent / data_dir
    errors.extend(validate_dataset(data_dir))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "configs",
        nargs="*",
        type=Path,
        default=sorted((ROOT / "gemma4" / "scripts").glob("train_config*.yaml")),
    )
    args = parser.parse_args()

    errors: list[str] = []
    checked = 0
    for config in args.configs:
        cfg = load_config(config)
        if cfg.get("model") in GEMMA4_NO_THINKING_MODELS:
            checked += 1
        errors.extend(validate_config(config))

    if errors:
        for error in errors:
            print(f"fail: {error}")
        return 1
    print(f"ok: Gemma 4 no-thinking dataset format ({checked} configs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
