#!/usr/bin/env python3
"""Validate that the tracked mem0 benchmark index table is current."""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVAL_ROOT = Path("/Volumes/PortableSSD/hermes-evals")
DEFAULT_INDEX = ROOT / "reports/benchmark/mem0/index.md"
BENCHMARK_DIRS = (
    "mem0-memory-benchmark",
    "embedding-benchmark",
    "mem0-extraction-benchmark",
    "mem0-isolated-fixture-rerank",
    "mem0-reranking-replay",
    "mem0-reranking-benchmark",
    "mem0-retriever-benchmark",
)


def collect_summary_paths(eval_root: Path) -> list[Path]:
    paths: list[Path] = []
    for dirname in BENCHMARK_DIRS:
        paths.extend(sorted((eval_root / dirname).glob("*/summary.json")))
    return paths


def extract_table(markdown: str) -> str:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("| Kind | Run ID |"):
            return "\n".join(lines[index:]).rstrip() + "\n"
    raise ValueError("missing mem0 benchmark index table")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def assert_same(expected: Path, actual: Path, failures: list[str]) -> None:
    expected_table = extract_table(expected.read_text(encoding="utf-8"))
    actual_table = extract_table(actual.read_text(encoding="utf-8"))
    if expected_table != actual_table:
        failures.append(
            f"{display_path(expected)} table is stale; regenerate with scripts/summarize_mem0_benchmarks.py"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-root", type=Path, default=DEFAULT_EVAL_ROOT)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    args = parser.parse_args()

    if not args.eval_root.exists():
        print(f"ready: mem0 benchmark index skipped; {args.eval_root} not present")
        return 0
    if not args.index.exists():
        print(f"not ready: missing {args.index}")
        return 1

    summary_paths = collect_summary_paths(args.eval_root)
    if not summary_paths:
        print(f"ready: mem0 benchmark index skipped; no summary.json files under {args.eval_root}")
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        generated = Path(tmp) / "index.md"
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/summarize_mem0_benchmarks.py"),
                *map(str, summary_paths),
                "--output",
                str(generated),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode:
            print(f"not ready: failed to regenerate mem0 benchmark index: {result.stderr.strip() or result.stdout.strip()}")
            return result.returncode

        failures: list[str] = []
        assert_same(args.index, generated, failures)

    if failures:
        print("not ready: mem0 benchmark index")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("ready: mem0 benchmark index table is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
