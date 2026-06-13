#!/usr/bin/env python3
"""Validate tracked standard benchmark coverage reports are current."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "benchmark" / "standard-coverage"
DEFAULT_REPORTS = (
    REPORT_DIR / "qwen3-v4-targeted-standard-coverage-20260526.json",
    REPORT_DIR / "qwen3-v6-free-text-copy-standard-coverage-20260613.json",
)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def assert_same(expected: Path, actual: Path, failures: list[str]) -> None:
    if expected.read_text(encoding="utf-8") != actual.read_text(encoding="utf-8"):
        failures.append(f"{display_path(actual)} is stale; regenerate it")


def validate_report(json_report: Path, failures: list[str]) -> None:
    md_report = json_report.with_suffix(".md")
    for path in (json_report, md_report):
        if not path.exists():
            failures.append(f"missing {display_path(path)}")
    if failures:
        return

    data = json.loads(json_report.read_text(encoding="utf-8"))
    created_at = str(data.get("created_at") or "")
    candidate = str(data.get("candidate") or "")
    run_id = str(data.get("run_id") or json_report.stem)
    if not created_at:
        failures.append(f"{display_path(json_report)} has no created_at timestamp")
    if not candidate:
        failures.append(f"{display_path(json_report)} has no candidate")
    if not data.get("items"):
        failures.append(f"{display_path(json_report)} has no coverage items")
    if failures:
        return

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        expected_json = tmpdir / json_report.name
        expected_md = tmpdir / md_report.name
        subprocess.run(
            [
                sys.executable,
                "scripts/check_standard_benchmark_coverage.py",
                "--candidate",
                candidate,
                "--run-id",
                run_id,
                "--json-output",
                str(expected_json),
                "--md-output",
                str(expected_md),
                "--created-at",
                created_at,
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        assert_same(expected_json, json_report, failures)
        assert_same(expected_md, md_report, failures)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports", type=Path, nargs="*", default=list(DEFAULT_REPORTS))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    for report in args.reports:
        validate_report(report, failures)

    if failures:
        print("not ready: standard benchmark coverage reports")
        for item in failures:
            print(f"- {item}")
        return 1

    print("ready: standard benchmark coverage reports are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
