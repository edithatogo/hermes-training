#!/usr/bin/env python3
"""Convert the local tool-call benchmark suite into strict chat training splits."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_suite(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError(f"{path}: expected a non-empty JSON array")
    return data


def tool_call_text(expected: dict[str, Any]) -> str:
    mode = expected.get("mode")
    if mode == "tool_calls":
        calls = expected.get("tool_calls")
        if not isinstance(calls, list) or not calls:
            raise ValueError("tool_calls mode requires non-empty tool_calls")
        chunks = []
        for call in calls:
            payload = {
                "name": call["name"],
                "arguments": call["arguments"],
            }
            chunks.append(f"<tool_call>{json.dumps(payload, separators=(',', ':'))}</tool_call>")
        return "".join(chunks)
    if mode == "text":
        return "I cannot use the requested tool because it is not available in the provided tool list."
    raise ValueError(f"unsupported expected.mode={mode!r}")


def training_row(case: dict[str, Any]) -> dict[str, Any]:
    messages = case.get("messages")
    expected = case.get("expected")
    if not isinstance(messages, list) or not isinstance(expected, dict):
        raise ValueError(f"{case.get('id', '<unknown>')}: missing messages or expected")
    row_messages = [{"role": str(msg["role"]), "content": str(msg["content"])} for msg in messages]
    row_messages.append({"role": "assistant", "content": tool_call_text(expected)})
    return {
        "id": f"{case['id']}-strict-target",
        "category": case.get("category", "tool_call"),
        "source": "benchmarks/tool_call_local/suite.json",
        "messages": row_messages,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=Path("benchmarks/tool_call_local/suite.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("gemma4/data/tool_call_splits"))
    parser.add_argument("--raw-output", type=Path, default=Path("gemma4/data/tool_call_seed/tool_call_seed.jsonl"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = [training_row(case) for case in load_suite(args.suite)]
    categories = sorted({str(row["category"]) for row in rows})
    print(f"rows: {len(rows)}")
    print(f"categories: {', '.join(categories)}")
    print(f"output_dir: {args.output_dir}")
    if args.dry_run:
        return 0

    write_jsonl(args.raw_output, rows)
    for split in ("train", "val", "valid", "test"):
        write_jsonl(args.output_dir / f"{split}.jsonl", rows)
        print(f"wrote {len(rows)} rows to {args.output_dir / f'{split}.jsonl'}")
    print(f"wrote raw seed rows to {args.raw_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
