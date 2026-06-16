#!/usr/bin/env python3
"""Validate generated cloud blocker reports against the current preflight state."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PREFLIGHT = ROOT / "reports/cloud/backend-preflight-20260613.json"
DEFAULT_CHECKLIST_JSON = ROOT / "reports/cloud/backend-unblock-checklist-20260613.json"
DEFAULT_CHECKLIST_MD = ROOT / "reports/cloud/backend-unblock-checklist-20260613.md"
DEFAULT_MATRIX_JSON = ROOT / "reports/cloud/active-blocked-track-matrix-20260613.json"
DEFAULT_MATRIX_MD = ROOT / "reports/cloud/active-blocked-track-matrix-20260613.md"

REQUIRED_TRACKS = {
}


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def arg_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def run_generator(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)


def assert_same(expected: Path, actual: Path, failures: list[str]) -> None:
    if expected.read_text() != actual.read_text():
        failures.append(f"{display_path(actual)} is stale; regenerate it")


def validate_semantics(matrix_path: Path, checklist_path: Path, failures: list[str]) -> None:
    matrix = load_json(matrix_path)
    checklist = load_json(checklist_path)
    rows = matrix.get("rows", [])
    items = checklist.get("items", [])

    if not rows:
        if REQUIRED_TRACKS:
            failures.append(f"{display_path(matrix_path)} has no blocked track rows")
        return

    checklist_backends = {item.get("backend") for item in items}
    row_tracks = {row.get("track_id") for row in rows}
    missing = sorted(REQUIRED_TRACKS - row_tracks)
    if missing:
        failures.append(f"{display_path(matrix_path)} is missing blocked tracks: {', '.join(missing)}")

    for row in rows:
        track = row.get("track_id", "<unknown>")
        backend = row.get("backend")
        if backend not in checklist_backends:
            failures.append(f"{track} references backend {backend!r} absent from checklist")
        if not row.get("blocker"):
            failures.append(f"{track} has no blocker summary")
        if not row.get("next_task"):
            failures.append(f"{track} has no next task")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument("--checklist-json", type=Path, default=DEFAULT_CHECKLIST_JSON)
    parser.add_argument("--checklist-md", type=Path, default=DEFAULT_CHECKLIST_MD)
    parser.add_argument("--matrix-json", type=Path, default=DEFAULT_MATRIX_JSON)
    parser.add_argument("--matrix-md", type=Path, default=DEFAULT_MATRIX_MD)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    required = [
        args.preflight,
        args.checklist_json,
        args.checklist_md,
        args.matrix_json,
        args.matrix_md,
    ]
    for path in required:
        if not path.exists():
            failures.append(f"missing {display_path(path)}")

    if not failures:
        validate_semantics(args.matrix_json, args.checklist_json, failures)

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected_checklist_json = tmpdir / "backend-unblock-checklist.json"
            expected_checklist_md = tmpdir / "backend-unblock-checklist.md"
            expected_matrix_json = tmpdir / "active-blocked-track-matrix.json"
            expected_matrix_md = tmpdir / "active-blocked-track-matrix.md"

            run_generator(
                [
                    sys.executable,
                    "scripts/build_cloud_unblock_checklist.py",
                    "--preflight",
                    arg_path(args.preflight),
                    "--json-output",
                    str(expected_checklist_json),
                    "--markdown-output",
                    str(expected_checklist_md),
                ]
            )
            run_generator(
                [
                    sys.executable,
                    "scripts/build_blocked_track_matrix.py",
                    "--checklist",
                    arg_path(args.checklist_json),
                    "--json-output",
                    str(expected_matrix_json),
                    "--markdown-output",
                    str(expected_matrix_md),
                ]
            )
            assert_same(expected_checklist_json, args.checklist_json, failures)
            assert_same(expected_checklist_md, args.checklist_md, failures)
            assert_same(expected_matrix_json, args.matrix_json, failures)
            assert_same(expected_matrix_md, args.matrix_md, failures)

    if failures:
        print("not ready: cloud blocker reports")
        for item in failures:
            print(f"- {item}")
        return 1

    print("ready: cloud blocker reports are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
