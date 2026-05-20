#!/usr/bin/env python3
"""Audit Hermes-local eval prompts for category coverage."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


DEFAULT_MINIMUMS = {
    "tool_use": 25,
    "code": 20,
    "long_context": 15,
    "reasoning": 15,
    "safety": 10,
    "factual": 10,
    "formatting": 5,
}


def load_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open() as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(row.get("prompt"), str) or not row["prompt"].strip():
                raise ValueError(f"{path}:{lineno}: missing prompt")
            if not isinstance(row.get("category"), str) or not row["category"].strip():
                raise ValueError(f"{path}:{lineno}: missing category")
            rows.append(row)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompts", type=Path, nargs="+")
    parser.add_argument("--min-total", type=int, default=100)
    parser.add_argument("--strict", action="store_true", help="Return non-zero when coverage is below target.")
    args = parser.parse_args()

    failed = False
    for path in args.prompts:
        rows = load_jsonl(path)
        counts = Counter(str(row["category"]) for row in rows)
        print(f"\n== {path}")
        print(f"total: {len(rows)}")
        for category, count in sorted(counts.items()):
            print(f"{category}: {count}")

        if len(rows) < args.min_total:
            failed = True
            print(f"gap: total prompts {len(rows)} < {args.min_total}")
        for category, minimum in DEFAULT_MINIMUMS.items():
            actual = counts.get(category, 0)
            if actual < minimum:
                failed = True
                print(f"gap: {category} {actual} < {minimum}")

    if failed and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
