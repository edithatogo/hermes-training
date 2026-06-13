#!/usr/bin/env python3
"""Materialize Gemma 4 no-thinking datasets with an empty thought channel."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


EMPTY_THOUGHT_CHANNEL = "<|channel>thought\n<channel|>"
SPLIT_NAMES = ("train", "val", "valid", "test")


def assistant_has_empty_channel(content: str) -> bool:
    return content.startswith(EMPTY_THOUGHT_CHANNEL)


def add_empty_channel(content: str) -> str:
    if assistant_has_empty_channel(content):
        return content
    return f"{EMPTY_THOUGHT_CHANNEL}{content}"


def transform_record(record: dict[str, Any]) -> tuple[dict[str, Any], int]:
    messages = record.get("messages")
    if not isinstance(messages, list):
        raise ValueError("record is missing a messages list")

    changed = 0
    transformed: list[dict[str, Any]] = []
    for message in messages:
        if not isinstance(message, dict):
            raise ValueError("message is not an object")
        role = message.get("role")
        content = message.get("content")
        if role == "assistant":
            if not isinstance(content, str):
                raise ValueError("assistant message content is not a string")
            new_message = dict(message)
            new_content = add_empty_channel(content)
            if new_content != content:
                changed += 1
            new_message["content"] = new_content
            transformed.append(new_message)
        else:
            transformed.append(dict(message))

    output = dict(record)
    output["messages"] = transformed
    return output, changed


def transform_file(source: Path, target: Path) -> tuple[int, int]:
    rows = 0
    changed_messages = 0
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("r", encoding="utf-8") as src, target.open("w", encoding="utf-8") as dst:
        for line_number, line in enumerate(src, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{source}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{source}:{line_number}: record is not an object")
            transformed, changed = transform_record(record)
            rows += 1
            changed_messages += changed
            dst.write(json.dumps(transformed, ensure_ascii=False) + "\n")
    return rows, changed_messages


def materialize_dataset(source_dir: Path, target_dir: Path) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = {}
    for split in SPLIT_NAMES:
        source = source_dir / f"{split}.jsonl"
        if not source.exists():
            continue
        rows, changed = transform_file(source, target_dir / f"{split}.jsonl")
        summary[split] = {"rows": rows, "assistant_messages_prefixed": changed}
    if not summary:
        raise ValueError(f"no split JSONL files found in {source_dir}")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--target-dir", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()

    try:
        summary = materialize_dataset(args.source_dir, args.target_dir)
    except ValueError as exc:
        sys.exit(f"error: {exc}")

    payload = {
        "source_dir": str(args.source_dir),
        "target_dir": str(args.target_dir),
        "empty_thought_channel": EMPTY_THOUGHT_CHANNEL,
        "splits": summary,
    }
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
