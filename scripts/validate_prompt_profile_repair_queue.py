#!/usr/bin/env python3
"""Validate the generated prompt/profile repair queue is current."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STEM = ROOT / "reports/benchmark/coverage/prompt-profile-repair-queue-20260614"
DEFAULT_JSON = DEFAULT_STEM.with_suffix(".json")
DEFAULT_MD = DEFAULT_STEM.with_suffix(".md")
MIN_EXPECTED_ROWS = 10


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
    parser.add_argument("--output-stem", type=Path, default=DEFAULT_STEM)
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
        rows = data.get("rows", [])
        created_at = str(data.get("created_at") or "")
        if not isinstance(rows, list) or len(rows) < MIN_EXPECTED_ROWS:
            failures.append(f"{display_path(args.json_report)} has too few repair rows")
        if not created_at:
            failures.append(f"{display_path(args.json_report)} has no created_at timestamp")
        for row in rows if isinstance(rows, list) else []:
            if not row.get("repair_hypothesis"):
                failures.append(f"{row.get('id', '<unknown>')} has no repair hypothesis")
            command = str(row.get("next_command", ""))
            if "--require-no-extra-tool-text" not in command:
                failures.append(f"{row.get('id', '<unknown>')} command is missing strict no-extra-text scoring")

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            output_stem = Path(tmp) / args.output_stem.name
            subprocess.run(
                [
                    sys.executable,
                    "scripts/build_prompt_profile_repair_queue.py",
                    "--output-stem",
                    str(output_stem),
                    "--created-at",
                    created_at,
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            assert_same(output_stem.with_suffix(".json"), args.json_report, failures)
            assert_same(output_stem.with_suffix(".md"), args.markdown_report, failures)

    if failures:
        print("not ready: prompt/profile repair queue")
        for item in failures:
            print(f"- {item}")
        return 1
    print("ready: prompt/profile repair queue is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
