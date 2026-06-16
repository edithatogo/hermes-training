#!/usr/bin/env python3
"""Validate the tracked RULER long-context preflight report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-ruler-long-context-preflight-20260616.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-ruler-long-context-preflight-20260616.md"
REQUIRED_STATUS = {"blocked-ruler-preflight", "ready-to-run"}


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
    if data.get("suite") != "ruler-long-context":
        failures.append(f"{display_path(report_path)} suite must be ruler-long-context")
    if data.get("run_id") != "qwen3-v4-peft-ruler-long-context-20260616":
        failures.append(f"{display_path(report_path)} run_id is wrong")
    if data.get("status") not in REQUIRED_STATUS:
        failures.append(f"{display_path(report_path)} status must be one of {sorted(REQUIRED_STATUS)}")
    if not str(data.get("output_root", "")).startswith("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/"):
        failures.append(f"{display_path(report_path)} output_root must be RULER SSD-backed")
    context = data.get("context_decision", {})
    if context.get("initial_max_seq_length") != 4096:
        failures.append(f"{display_path(report_path)} must start with max_seq_length 4096")
    if context.get("ladder") != [4096, 8192, 16384]:
        failures.append(f"{display_path(report_path)} must record the context ladder")
    checks = data.get("checks")
    if not isinstance(checks, dict):
        failures.append(f"{display_path(report_path)} checks must be an object")
    else:
        for key in (
            "queue_item_present",
            "suite_status_missing",
            "run_id_matches",
            "output_root_ssd_backed",
            "command_uses_ruler_module",
            "command_uses_initial_context",
            "command_omits_context_placeholder",
            "command_writes_ctx4096",
            "benchmark_python_present",
            "ruler_module_present",
        ):
            if key not in checks:
                failures.append(f"{display_path(report_path)} missing check {key}")
    command = str(data.get("local_command", ""))
    if "<context>" in command:
        failures.append(f"{display_path(report_path)} command must not contain <context>")
    if "--max_seq_length 4096" not in command or "ctx4096" not in command:
        failures.append(f"{display_path(report_path)} command must target ctx4096")
    if "not scored benchmark evidence" not in str(data.get("decision", "")):
        failures.append(f"{display_path(report_path)} must preserve non-score boundary")
    if "No public broad benchmark claim" not in str(data.get("publication_boundary", "")):
        failures.append(f"{display_path(report_path)} must preserve publication boundary")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()
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
            expected_json = tmpdir / "ruler-preflight.json"
            expected_md = tmpdir / "ruler-preflight.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/check_ruler_long_context_preflight.py",
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
        print("not ready: RULER long-context preflight")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: RULER long-context preflight")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
