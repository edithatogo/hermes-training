#!/usr/bin/env python3
"""Validate the selected prompt/profile repair dry-run report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/coverage/prompt-profile-repair-selection-20260614.json"
DEFAULT_MD = ROOT / "reports/benchmark/coverage/prompt-profile-repair-selection-20260614.md"
DEFAULT_CANDIDATE = "Qwen/Qwen3.5-0.8B"
DEFAULT_VARIANT = "strict-suffix-copy-exact"


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

    if not failures:
        data = json.loads(args.json_report.read_text(encoding="utf-8"))
        if data.get("status") != "dry-run":
            failures.append(f"{display_path(args.json_report)} must remain dry-run by default")
        if data.get("execute"):
            failures.append(f"{display_path(args.json_report)} unexpectedly records execute=true")
        if data.get("candidate") != DEFAULT_CANDIDATE or data.get("variant") != DEFAULT_VARIANT:
            failures.append(f"{display_path(args.json_report)} selects the wrong default experiment")
        command = str(data.get("command", ""))
        if "--require-no-extra-tool-text" not in command:
            failures.append("selected command is missing strict no-extra-tool-text scoring")
        if "No download here" not in command:
            failures.append("selected command is missing no-download boundary")
        if "run_local_pilot_benchmark.py" not in command:
            failures.append("selected default should use the local runner")

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected_json = tmpdir / "selection.json"
            expected_md = tmpdir / "selection.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/select_prompt_profile_repair_experiment.py",
                    "--candidate",
                    DEFAULT_CANDIDATE,
                    "--variant",
                    DEFAULT_VARIANT,
                    "--json-output",
                    str(expected_json),
                    "--markdown-output",
                    str(expected_md),
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            assert_same(expected_json, args.json_report, failures)
            assert_same(expected_md, args.markdown_report, failures)

    if failures:
        print("not ready: prompt/profile repair selection")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: prompt/profile repair selection is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
