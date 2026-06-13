#!/usr/bin/env python3
"""Validate the tracked mem0 benchmark evidence validation report is current."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVAL_ROOT = Path("/Volumes/PortableSSD/hermes-evals")
DEFAULT_REPORT = ROOT / "reports" / "benchmark" / "mem0" / "validation" / "mem0-evidence-validation-20260526.json"


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
    parser.add_argument("--eval-root", type=Path, default=DEFAULT_EVAL_ROOT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    if not args.eval_root.exists():
        print(f"ready: mem0 benchmark evidence report skipped; {args.eval_root} not present")
        return 0
    if not args.report.exists():
        failures.append(f"missing {display_path(args.report)}")

    created_at = ""
    if not failures:
        data = json.loads(args.report.read_text(encoding="utf-8"))
        created_at = str(data.get("created_at") or "")
        if not created_at:
            failures.append(f"{display_path(args.report)} has no created_at timestamp")
        if data.get("status") != "passed":
            failures.append(f"{display_path(args.report)} status is not passed")
        if not data.get("items"):
            failures.append(f"{display_path(args.report)} has no validation items")

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            expected = Path(tmp) / "mem0-evidence-validation.json"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/check_mem0_benchmark_evidence.py",
                    "--eval-root",
                    str(args.eval_root),
                    "--output",
                    str(expected),
                    "--created-at",
                    created_at,
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            assert_same(expected, args.report, failures)

    if failures:
        print("not ready: mem0 benchmark evidence report")
        for item in failures:
            print(f"- {item}")
        return 1

    print("ready: mem0 benchmark evidence report is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
