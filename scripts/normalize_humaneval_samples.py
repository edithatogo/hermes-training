#!/usr/bin/env python3
"""Normalize generated HumanEval JSONL completions in place."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from generate_humaneval_mlx_solutions import clean_completion


def normalize_samples(path: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    changed = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            before = str(row.get("completion", ""))
            after = clean_completion(before)
            if after != before:
                changed += 1
            row["completion"] = after
            rows.append(row)

    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    tmp_path.replace(path)
    return {"path": str(path), "rows": len(rows), "changed_rows": changed}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("samples", type=Path)
    args = parser.parse_args()
    print(json.dumps(normalize_samples(args.samples), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
