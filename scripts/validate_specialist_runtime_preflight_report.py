#!/usr/bin/env python3
"""Validate the tracked specialist runtime preflight report is current."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports" / "runtime" / "specialist-runtime-preflight-20260526.json"
DEFAULT_MD = ROOT / "reports" / "runtime" / "specialist-runtime-preflight-20260526.md"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def assert_same(expected: Path, actual: Path, failures: list[str]) -> None:
    if expected.read_text(encoding="utf-8") != actual.read_text(encoding="utf-8"):
        failures.append(f"{display_path(actual)} is stale; regenerate it")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MD)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    for path in (args.json_report, args.markdown_report):
        if not path.exists():
            failures.append(f"missing {display_path(path)}")

    created_at = ""
    if not failures:
        data = json.loads(args.json_report.read_text(encoding="utf-8"))
        created_at = str(data.get("created_at") or "")
        if not created_at:
            failures.append(f"{display_path(args.json_report)} has no created_at timestamp")
        if not data.get("items"):
            failures.append(f"{display_path(args.json_report)} has no preflight items")
        if data.get("status") not in {"passed", "empty"}:
            failures.append(f"{display_path(args.json_report)} has invalid status {data.get('status')!r}")

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected_json = tmpdir / "specialist-runtime-preflight.json"
            expected_md = tmpdir / "specialist-runtime-preflight.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/check_specialist_runtime_preflight.py",
                    "--json-output",
                    str(expected_json),
                    "--output",
                    str(expected_md),
                    "--created-at",
                    created_at,
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            assert_same(expected_json, args.json_report, failures)
            assert_same(expected_md, args.markdown_report, failures)

    if failures:
        print("not ready: specialist runtime preflight report")
        for item in failures:
            print(f"- {item}")
        return 1

    print("ready: specialist runtime preflight report is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
