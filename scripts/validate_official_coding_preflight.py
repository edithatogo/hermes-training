#!/usr/bin/env python3
"""Validate the tracked official coding preflight report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-coding-preflight-20260616.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-coding-preflight-20260616.md"
REQUIRED_STATUS = {"blocked-coding-preflight", "ready-to-evaluate"}


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def assert_same(expected: Path, actual: Path, failures: list[str]) -> None:
    if expected.read_text(encoding="utf-8") != actual.read_text(encoding="utf-8"):
        failures.append(f"{display_path(actual)} is stale; regenerate it")


def validate_payload(data: dict, report_path: Path) -> list[str]:
    failures: list[str] = []
    if data.get("suite") != "official-coding":
        failures.append(f"{display_path(report_path)} suite must be official-coding")
    if data.get("run_id") != "qwen3-v4-peft-official-coding-20260616":
        failures.append(f"{display_path(report_path)} run_id is wrong")
    if data.get("status") not in REQUIRED_STATUS:
        failures.append(f"{display_path(report_path)} status must be one of {sorted(REQUIRED_STATUS)}")
    if not str(data.get("output_root", "")).startswith("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/"):
        failures.append(f"{display_path(report_path)} output_root must be coding SSD-backed")
    checks = data.get("checks")
    if not isinstance(checks, dict):
        failures.append(f"{display_path(report_path)} checks must be an object")
    else:
        for key in (
            "queue_item_present",
            "suite_status_missing",
            "run_id_matches",
            "output_root_ssd_backed",
            "command_uses_evalplus_module",
            "command_uses_positional_humaneval",
            "command_uses_samples",
            "command_omits_stale_model_flag",
            "evalplus_cli_executable",
            "evalplus_module_present",
            "human_eval_module_present",
            "generated_solutions_present",
        ):
            if key not in checks:
                failures.append(f"{display_path(report_path)} missing check {key}")
        if not checks.get("command_omits_stale_model_flag"):
            failures.append(f"{display_path(report_path)} still contains stale EvalPlus --model/--dataset command shape")
    if "not scored benchmark evidence" not in str(data.get("decision", "")):
        failures.append(f"{display_path(report_path)} must preserve non-score boundary")
    if "No public broad benchmark claim" not in str(data.get("publication_boundary", "")):
        failures.append(f"{display_path(report_path)} must preserve publication boundary")
    return failures


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
        failures.extend(validate_payload(data, args.json_report))

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected_json = tmpdir / "coding-preflight.json"
            expected_md = tmpdir / "coding-preflight.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/check_official_coding_preflight.py",
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
        print("not ready: official coding preflight report")
        for item in failures:
            print(f"- {item}")
        return 1
    print("ready: official coding preflight report is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
