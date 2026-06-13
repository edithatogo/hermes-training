#!/usr/bin/env python3
"""Validate the generated mem0 candidate execution queue is current."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "reports" / "model-radar" / "mem0-candidate-queue.md"


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
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    if not args.output.exists():
        failures.append(f"missing {display_path(args.output)}")

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            expected = Path(tmp) / "mem0-candidate-queue.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/build_mem0_candidate_queue.py",
                    "--output",
                    str(expected),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            assert_same(expected, args.output, failures)

    if failures:
        print("not ready: mem0 candidate queue")
        for item in failures:
            print(f"- {item}")
        return 1

    print("ready: mem0 candidate queue is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
