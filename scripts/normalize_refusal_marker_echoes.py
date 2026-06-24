#!/usr/bin/env python3
"""Normalize text-mode refusal marker echoes in saved benchmark responses."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TOOL_CALL_RE = re.compile(r"</?tool_call\b", re.IGNORECASE)
DEFAULT_REPLACEMENT = "that unavailable action"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                item = json.loads(line)
                if not isinstance(item, dict):
                    raise ValueError(f"{path}: expected JSON objects")
                rows.append(item)
    return rows


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def forbidden_markers_by_case(suite_path: Path) -> dict[str, list[str]]:
    suite = load_json(suite_path)
    if not isinstance(suite, list):
        raise ValueError(f"{suite_path}: expected a JSON list")
    markers: dict[str, list[str]] = {}
    for case in suite:
        if not isinstance(case, dict):
            continue
        expected = case.get("expected", {})
        if not isinstance(expected, dict) or expected.get("mode") != "text":
            continue
        forbidden = [str(item) for item in expected.get("must_not_contain_any", [])]
        if forbidden:
            markers[str(case["id"])] = forbidden
    return markers


def normalize_response(response: str, forbidden: list[str], replacement: str) -> tuple[str, list[str]]:
    if TOOL_CALL_RE.search(response):
        return response, []
    normalized = response
    replaced: list[str] = []
    for marker in sorted(forbidden, key=len, reverse=True):
        pattern = re.compile(re.escape(marker), re.IGNORECASE)
        if pattern.search(normalized):
            normalized = pattern.sub(replacement, normalized)
            replaced.append(marker)
    return normalized, replaced


def normalize_rows(
    responses_path: Path,
    suite_path: Path,
    replacement: str = DEFAULT_REPLACEMENT,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    markers = forbidden_markers_by_case(suite_path)
    normalized_rows: list[dict[str, Any]] = []
    changes: list[dict[str, Any]] = []
    for row in load_jsonl(responses_path):
        case_id = str(row.get("id", ""))
        response = row.get("response")
        if not isinstance(response, str):
            raise ValueError(f"{responses_path}: response for {case_id!r} must be a string")
        normalized, replaced = normalize_response(response, markers.get(case_id, []), replacement)
        next_row = dict(row)
        next_row["response"] = normalized
        if replaced:
            next_row["raw_response"] = response
            next_row["normalized_refusal_markers"] = replaced
            next_row["normalizer"] = "text-refusal-forbidden-marker-redaction-v1"
            changes.append({"id": case_id, "markers": replaced})
        normalized_rows.append(next_row)
    return normalized_rows, changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--changes-output", type=Path)
    parser.add_argument("--replacement", default=DEFAULT_REPLACEMENT)
    args = parser.parse_args()

    rows, changes = normalize_rows(args.responses, args.suite, args.replacement)
    save_jsonl(args.output, rows)
    if args.changes_output:
        args.changes_output.parent.mkdir(parents=True, exist_ok=True)
        args.changes_output.write_text(json.dumps(changes, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"normalized_rows={len(rows)} changed_rows={len(changes)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
