#!/usr/bin/env python3
"""Audit JSONL chat split token counts with the target model tokenizer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from mlx_lm import load


def percentile(values: list[int], pct: float) -> int:
    if not values:
        return 0
    idx = min(len(values) - 1, max(0, int(len(values) * pct) - 1))
    return values[idx]


def audit_split(path: Path, tokenizer) -> dict[str, int | float]:
    lengths: list[int] = []
    for line in path.open(encoding="utf-8"):
        if not line.strip():
            continue
        data = json.loads(line)
        tokens = tokenizer.apply_chat_template(data["messages"], return_dict=False)
        lengths.append(len(tokens))

    lengths.sort()
    total = sum(lengths)
    rows = len(lengths)
    return {
        "rows": rows,
        "tokens": total,
        "avg_tokens": round(total / rows, 1) if rows else 0,
        "p50": percentile(lengths, 0.50),
        "p95": percentile(lengths, 0.95),
        "max": lengths[-1] if lengths else 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit token counts for chat JSONL splits.")
    parser.add_argument("--model", required=True, help="Model or local path used for tokenization.")
    parser.add_argument("--data", type=Path, required=True, help="Directory with train/valid/test JSONL files.")
    parser.add_argument("--splits", nargs="+", default=["train", "valid", "test"])
    args = parser.parse_args()

    _, tokenizer = load(args.model)
    for split in args.splits:
        path = args.data / f"{split}.jsonl"
        if not path.exists():
            print(f"{split}: missing {path}")
            continue
        result = audit_split(path, tokenizer)
        print(f"{split}: {json.dumps(result, sort_keys=True)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
