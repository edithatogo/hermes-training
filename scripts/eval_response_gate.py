#!/usr/bin/env python3
"""Fail release checks when eval outputs collapse or become too terse."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def load_results(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            response = row.get("response")
            if not isinstance(response, str):
                raise ValueError(f"{path}:{lineno}: missing string response")
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no result rows")
    return rows


def word_count(row: dict[str, object]) -> int:
    value = row.get("response_length")
    if isinstance(value, int):
        return value
    return len(str(row.get("response", "")).split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="Evaluation JSONL output.")
    parser.add_argument("--min-avg-words", type=float, default=20.0)
    parser.add_argument("--max-empty-rate", type=float, default=0.15)
    parser.add_argument("--min-category-avg-words", type=float, default=10.0)
    parser.add_argument("--strict", action="store_true", help="Return non-zero when a gate fails.")
    args = parser.parse_args()

    rows = load_results(args.results)
    counts = [word_count(row) for row in rows]
    empty_count = sum(1 for row in rows if not str(row.get("response", "")).strip())
    avg_words = sum(counts) / len(counts)
    empty_rate = empty_count / len(rows)

    by_category: dict[str, list[int]] = defaultdict(list)
    for row, count in zip(rows, counts, strict=True):
        by_category[str(row.get("category", "general"))].append(count)

    print(f"results: {args.results}")
    print(f"rows: {len(rows)}")
    print(f"avg_words: {avg_words:.2f}")
    print(f"empty_rate: {empty_rate:.3f}")

    failed = False
    if avg_words < args.min_avg_words:
        failed = True
        print(f"gap: avg_words {avg_words:.2f} < {args.min_avg_words:.2f}")
    if empty_rate > args.max_empty_rate:
        failed = True
        print(f"gap: empty_rate {empty_rate:.3f} > {args.max_empty_rate:.3f}")

    category_counts = Counter()
    for category, values in sorted(by_category.items()):
        category_avg = sum(values) / len(values)
        category_counts[category] = len(values)
        print(f"{category}: rows={len(values)} avg_words={category_avg:.2f}")
        if category_avg < args.min_category_avg_words:
            failed = True
            print(f"gap: {category} avg_words {category_avg:.2f} < {args.min_category_avg_words:.2f}")

    if failed and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
