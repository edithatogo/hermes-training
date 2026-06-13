#!/usr/bin/env python3
"""Validate the generated scorecard offload readiness report is current."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/cloud/qwen3-v4-scorecard-offload-readiness-20260613.json"
DEFAULT_MD = ROOT / "reports/cloud/qwen3-v4-scorecard-offload-readiness-20260613.md"


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
        if data.get("status") not in {"ready", "blocked"}:
            failures.append(f"{display_path(args.json_report)} has invalid status {data.get('status')!r}")
        if not data.get("adapter_classification"):
            failures.append(f"{display_path(args.json_report)} has no adapter classification")

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected_json = tmpdir / "scorecard-offload-readiness.json"
            expected_md = tmpdir / "scorecard-offload-readiness.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/check_scorecard_offload_readiness.py",
                    "--json-output",
                    str(expected_json),
                    "--markdown-output",
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
        print("not ready: scorecard offload readiness")
        for item in failures:
            print(f"- {item}")
        return 1

    print("ready: scorecard offload readiness is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
