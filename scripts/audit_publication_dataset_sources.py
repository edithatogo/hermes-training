#!/usr/bin/env python3
"""Summarize source provenance for a JSONL publication dataset bundle."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_rows(data_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(data_dir.glob("*.jsonl")):
        with path.open(encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                row = json.loads(line)
                row["_file"] = path.name
                row["_lineno"] = lineno
                rows.append(row)
    return rows


def base_source(row: dict[str, Any]) -> str:
    source = row.get("source")
    if not isinstance(source, str) or not source:
        return "strict_tool_call_seed"
    return source.removesuffix("+no_think_prompt")


def has_no_think(row: dict[str, Any]) -> bool:
    if str(row.get("source", "")).endswith("+no_think_prompt"):
        return True
    for message in row.get("messages", []):
        if isinstance(message, dict) and message.get("role") == "user":
            return str(message.get("content", "")).lstrip().startswith("/no_think")
    return False


def first_user(row: dict[str, Any]) -> str:
    for message in row.get("messages", []):
        if isinstance(message, dict) and message.get("role") == "user":
            return str(message.get("content", ""))
    return ""


def summarize(data_dir: Path) -> dict[str, Any]:
    rows = load_rows(data_dir)
    by_source = Counter(base_source(row) for row in rows)
    by_split = Counter(row["_file"] for row in rows)
    no_think = sum(1 for row in rows if has_no_think(row))
    examples: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        source = base_source(row)
        if len(examples[source]) >= 3:
            continue
        examples[source].append(
            {
                "id": str(row.get("id", "")),
                "split": str(row["_file"]).removesuffix(".jsonl"),
                "first_user": first_user(row)[:180],
            }
        )

    policy = {
        "strict_tool_call_seed": {
            "origin": "repo-authored mirrored strict local benchmark seed",
            "redistribution": "reviewed; allowed for GitHub evidence, but public dataset publication should disclose benchmark-seed overlap",
        },
        "strict_tool_call": {
            "origin": "repo-authored mirrored strict local benchmark seed with no-think prompt variants",
            "redistribution": "reviewed; allowed for GitHub evidence, but public dataset publication should disclose benchmark-seed overlap",
        },
        "strict_tool_call_expansion_v1": {
            "origin": "repo-authored deterministic synthetic expansion",
            "redistribution": "reviewed; no external corpus dependency identified",
        },
        "strict_tool_call_expansion_v2_format_guard": {
            "origin": "repo-authored deterministic synthetic format-guard expansion",
            "redistribution": "reviewed; no external corpus dependency identified",
        },
        "strict_tool_call_expansion_v4_targeted": {
            "origin": "repo-authored targeted synthetic rows from local failure analysis",
            "redistribution": "reviewed; no held-out prompt copying identified, but one generic held-out tool-name overlap remains disclosed",
        },
    }

    unknown_sources = sorted(set(by_source) - set(policy))
    return {
        "data_dir": str(data_dir),
        "rows": len(rows),
        "unique_ids": len({row.get("id") for row in rows}),
        "duplicate_id_count": len(rows) - len({row.get("id") for row in rows}),
        "rows_with_no_think_prompt": no_think,
        "source_counts": dict(sorted(by_source.items())),
        "split_counts": dict(sorted(by_split.items())),
        "source_examples": {key: value for key, value in sorted(examples.items())},
        "source_policy": policy,
        "unknown_sources": unknown_sources,
        "review_result": "blocked" if unknown_sources else "reviewed_with_caveats",
        "public_dataset_release": "blocked_pending_human_scope_approval",
        "adapter_release_source_gate": "source_review_complete_with_disclosed_caveats" if not unknown_sources else "blocked",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = summarize(args.data_dir)
    payload = json.dumps(summary, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 1 if summary["unknown_sources"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
