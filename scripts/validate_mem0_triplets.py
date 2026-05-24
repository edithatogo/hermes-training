#!/usr/bin/env python3
"""Validate mem0 contrastive triplet JSONL data."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


VALID_CATEGORIES = {"direct_recall", "recency_conflict", "distractor_resistance", "tool_state_recall", "doc_grounded"}


def validate_row(row: dict[str, Any], path: Path, lineno: int) -> list[str]:
    errors: list[str] = []
    prefix = f"{path}:{lineno}"
    required = {"id", "anchor", "positive", "negatives", "category"}
    missing = required - set(row)
    if missing:
        errors.append(f"{prefix}: missing {sorted(missing)}")
    for field in ("id", "anchor", "positive", "category"):
        if field in row and (not isinstance(row[field], str) or not row[field]):
            errors.append(f"{prefix}: {field} must be a non-empty string")
    negatives = row.get("negatives")
    if not isinstance(negatives, list) or not negatives or not all(isinstance(item, str) and item for item in negatives):
        errors.append(f"{prefix}: negatives must be a non-empty list of strings")
    if row.get("category") not in VALID_CATEGORIES:
        errors.append(f"{prefix}: unsupported category {row.get('category')!r}")
    if isinstance(negatives, list) and row.get("positive") in negatives:
        errors.append(f"{prefix}: positive must not also appear in negatives")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    failed = False
    seen_ids: set[str] = set()
    categories: Counter[str] = Counter()
    rows = 0
    for path in args.paths:
        with path.open(encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                rows += 1
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    print(f"{path}:{lineno}: invalid JSON: {exc}")
                    failed = True
                    continue
                if not isinstance(row, dict):
                    print(f"{path}:{lineno}: row must be an object")
                    failed = True
                    continue
                errors = validate_row(row, path, lineno)
                for error in errors:
                    print(error)
                failed = failed or bool(errors)
                row_id = row.get("id")
                if isinstance(row_id, str):
                    if row_id in seen_ids:
                        print(f"{path}:{lineno}: duplicate id {row_id}")
                        failed = True
                    seen_ids.add(row_id)
                category = row.get("category")
                if isinstance(category, str):
                    categories[category] += 1

    print(f"rows: {rows}")
    print(f"categories: {dict(categories)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

