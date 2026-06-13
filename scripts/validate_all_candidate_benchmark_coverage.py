#!/usr/bin/env python3
"""Validate the generated all-candidate benchmark coverage report is current."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ID = "all-candidate-benchmark-coverage-20260612"
DEFAULT_REPORT_DIR = ROOT / "reports" / "benchmark" / "coverage"
DEFAULT_JSON = DEFAULT_REPORT_DIR / f"{DEFAULT_RUN_ID}.json"
DEFAULT_MD = DEFAULT_REPORT_DIR / f"{DEFAULT_RUN_ID}.md"


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
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
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
        rows = data.get("rows", [])
        if not isinstance(rows, list) or not rows:
            failures.append(f"{display_path(args.json_report)} has no candidate rows")
        if not data.get("counts"):
            failures.append(f"{display_path(args.json_report)} has no coverage counts")
        if not created_at:
            failures.append(f"{display_path(args.json_report)} has no created_at timestamp")

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            subprocess.run(
                [
                    sys.executable,
                    "scripts/build_all_candidate_benchmark_coverage.py",
                    "--run-id",
                    args.run_id,
                    "--output-dir",
                    str(out),
                    "--created-at",
                    created_at,
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            assert_same(out / f"{args.run_id}.json", args.json_report, failures)
            assert_same(out / f"{args.run_id}.md", args.markdown_report, failures)

    if failures:
        print("not ready: all-candidate benchmark coverage")
        for item in failures:
            print(f"- {item}")
        return 1

    print("ready: all-candidate benchmark coverage is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
