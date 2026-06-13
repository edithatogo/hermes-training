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
DEFAULT_EXPERIMENTS = ROOT / "reports/benchmark/coverage/prompt-profile-repair-experiments-20260614.json"
DEFAULT_RESULTS = ROOT / "reports/benchmark/coverage/prompt-profile-repair-results-20260614.json"


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
    parser.add_argument("--experiments", type=Path, default=DEFAULT_EXPERIMENTS)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    return parser.parse_args()


def expected_default(experiments_path: Path, results_path: Path) -> dict[str, str | None]:
    experiments_data = json.loads(experiments_path.read_text(encoding="utf-8"))
    results_data = json.loads(results_path.read_text(encoding="utf-8"))
    completed = {
        (str(row.get("candidate")), str(row.get("variant")))
        for row in results_data.get("results", [])
        if isinstance(row, dict)
    }
    for experiment in experiments_data.get("experiments", []):
        if not isinstance(experiment, dict):
            continue
        key = (str(experiment.get("candidate")), str(experiment.get("variant")))
        if key not in completed:
            return {
                "candidate": key[0],
                "variant": key[1],
                "runner": str(experiment.get("runner", "")),
            }
    return {
        "candidate": None,
        "variant": None,
        "runner": "none",
    }


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    for path in (args.json_report, args.markdown_report, args.experiments, args.results):
        if not path.exists():
            failures.append(f"missing {display_path(path)}")

    expected: dict[str, str] | None = None
    if not failures:
        try:
            expected = expected_default(args.experiments, args.results)
        except Exception as exc:
            failures.append(f"could not derive expected default experiment: {exc}")

    if not failures:
        data = json.loads(args.json_report.read_text(encoding="utf-8"))
        if expected["runner"] == "none":
            if data.get("status") != "exhausted":
                failures.append(f"{display_path(args.json_report)} must record exhausted status when no experiments remain")
            if data.get("candidate") is not None or data.get("variant") is not None:
                failures.append(f"{display_path(args.json_report)} must not select a completed experiment")
            if data.get("execute"):
                failures.append(f"{display_path(args.json_report)} unexpectedly records execute=true")
        else:
            if data.get("status") != "dry-run":
                failures.append(f"{display_path(args.json_report)} must remain dry-run by default")
            if data.get("execute"):
                failures.append(f"{display_path(args.json_report)} unexpectedly records execute=true")
            if (
                data.get("candidate") != expected["candidate"]
                or data.get("variant") != expected["variant"]
                or data.get("runner") != expected["runner"]
            ):
                failures.append(f"{display_path(args.json_report)} selects the wrong default experiment")
            command = str(data.get("command", ""))
            if "--require-no-extra-tool-text" not in command:
                failures.append("selected command is missing strict no-extra-tool-text scoring")
            if "No download here" not in command:
                failures.append("selected command is missing no-download boundary")
            if expected["runner"] == "local" and "run_local_pilot_benchmark.py" not in command:
                failures.append("selected local default should use the local runner")
            if expected["runner"] == "endpoint" and "run_endpoint_pilot_benchmark.py" not in command:
                failures.append("selected endpoint default should use the endpoint runner")

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected_json = tmpdir / "selection.json"
            expected_md = tmpdir / "selection.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/select_prompt_profile_repair_experiment.py",
                    "--json-output",
                    str(expected_json),
                    "--markdown-output",
                    str(expected_md),
                ]
                + (
                    []
                    if expected["runner"] == "none"
                    else ["--candidate", str(expected["candidate"]), "--variant", str(expected["variant"])]
                ),
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
