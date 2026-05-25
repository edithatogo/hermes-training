#!/usr/bin/env python3
"""Materialize a cleaned JSONL dataset candidate from approved source classes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_ALLOWED_SOURCES = (
    "strict_tool_call_expansion_v1",
    "strict_tool_call_expansion_v2_format_guard",
    "strict_tool_call_expansion_v4_targeted",
)
DEFAULT_SPLIT_MAP = {
    "train": "train",
    "val": "validation",
    "test": "test",
}


def base_source(row: dict[str, Any]) -> str:
    source = row.get("source")
    if not isinstance(source, str) or not source:
        return "strict_tool_call_seed"
    return source.removesuffix("+no_think_prompt")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def materialize(
    input_dir: Path,
    output_dir: Path,
    *,
    allowed_sources: set[str],
    split_map: dict[str, str],
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "allowed_sources": sorted(allowed_sources),
        "splits": {},
        "excluded": {},
        "rows": 0,
        "unique_ids": 0,
    }
    ids: set[str] = set()

    for input_split, output_split in split_map.items():
        input_path = input_dir / f"{input_split}.jsonl"
        rows = load_jsonl(input_path)
        kept = [row for row in rows if base_source(row) in allowed_sources]
        excluded = [row for row in rows if base_source(row) not in allowed_sources]
        output_path = output_dir / f"{output_split}.jsonl"
        write_jsonl(output_path, kept)
        ids.update(str(row.get("id", "")) for row in kept)
        summary["rows"] += len(kept)
        summary["splits"][output_split] = {
            "input_split": input_split,
            "output_path": str(output_path),
            "rows": len(kept),
        }
        summary["excluded"][input_split] = {
            "rows": len(excluded),
            "sources": sorted({base_source(row) for row in excluded}),
        }

    summary["unique_ids"] = len(ids)
    summary["duplicate_id_count"] = summary["rows"] - summary["unique_ids"]
    return summary


def parse_source_list(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--allowed-sources",
        default=",".join(DEFAULT_ALLOWED_SOURCES),
        help="Comma-separated base source classes to include.",
    )
    parser.add_argument("--summary-output", type=Path)
    args = parser.parse_args()

    summary = materialize(
        args.input_dir,
        args.output_dir,
        allowed_sources=parse_source_list(args.allowed_sources),
        split_map=DEFAULT_SPLIT_MAP,
    )
    rendered = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.summary_output:
        args.summary_output.parent.mkdir(parents=True, exist_ok=True)
        args.summary_output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
