#!/usr/bin/env python3
"""Validate the Qwen3 v4 BFCL completion-suffix diagnostic report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-bfcl-completion-suffix-diagnostic-20260624.json"
DEFAULT_MD = DEFAULT_JSON.with_suffix(".md")
SSD_PREFIX = "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/"


def validate_payload(data: dict) -> list[str]:
    failures: list[str] = []
    if data.get("status") != "runtime-bridge-ready-for-bounded-rerun":
        failures.append("diagnostic must record runtime bridge readiness for a bounded rerun")
    if data.get("proxy_supports_completion_prompt_suffix") is not True:
        failures.append("proxy must support completion prompt suffix")
    if data.get("completion_prompt_suffix") != "<tool_call>":
        failures.append("completion suffix must be <tool_call> for the next BFCL gate")
    for key in (
        "clean_rerun",
        "serial_partial_without_suffix",
        "toolcall_prefix_micro_gate",
        "reasoning_bridge_micro_gate",
        "capped512_partial_without_suffix",
    ):
        run = data.get(key, {})
        if not str(run.get("run_root", "")).startswith(SSD_PREFIX):
            failures.append(f"{key} root must be SSD-backed")
        if int(run.get("total_rows", 0)) <= 0:
            failures.append(f"{key} must include generated rows")
        if int(run.get("blank_rows", 0)) <= 0:
            failures.append(f"{key} must record blank rows")
        if int(run.get("tool_like_rows", -1)) != 0:
            failures.append(f"{key} should not contain tool-like rows until a passing gate is recorded")
    direct_probe = data.get("text_prefix_direct_probe", {})
    if not str(direct_probe.get("path", "")).startswith(SSD_PREFIX):
        failures.append("text prefix direct probe path must be SSD-backed")
    if direct_probe.get("exists") is not True:
        failures.append("text prefix direct probe must exist")
    if direct_probe.get("text_starts_tool_call") is not True:
        failures.append("text prefix direct probe must start with <tool_call>")
    if direct_probe.get("text_contains_json_name") is not True:
        failures.append("text prefix direct probe must contain a JSON function name")
    if int(direct_probe.get("completion_text_prefix_count", 0)) <= 0:
        failures.append("text prefix direct probe must record completion text prefixing")
    serial = data.get("serial_partial_without_suffix", {})
    if int(serial.get("tool_like_rows", -1)) != 0:
        failures.append("serial partial without suffix should not contain tool-like rows")
    if data.get("gate", {}).get("passed") is not False:
        failures.append("diagnostic must not pass the BFCL model-quality gate")
    boundary = str(data.get("publication_boundary", ""))
    if "does not create a BFCL score claim" not in boundary:
        failures.append("publication boundary must block BFCL score claims")
    return failures


def validate_report(path: Path = DEFAULT_JSON, markdown_path: Path = DEFAULT_MD) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"]
    if not markdown_path.exists():
        failures.append(f"missing {markdown_path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    failures.extend(validate_payload(data))
    if markdown_path.exists() and "Completion-Suffix Diagnostic" not in markdown_path.read_text(encoding="utf-8"):
        failures.append("markdown report must describe the completion-suffix diagnostic")
    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            expected_json = Path(tmp) / "report.json"
            expected_md = Path(tmp) / "report.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/build_bfcl_completion_suffix_diagnostic_report.py",
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
            if expected_json.read_text(encoding="utf-8") != path.read_text(encoding="utf-8"):
                failures.append(f"{path.relative_to(ROOT)} is stale; regenerate it")
            if expected_md.read_text(encoding="utf-8") != markdown_path.read_text(encoding="utf-8"):
                failures.append(f"{markdown_path.relative_to(ROOT)} is stale; regenerate it")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()
    failures = validate_report(args.report, args.markdown_report)
    if failures:
        print("not ready: BFCL completion-suffix diagnostic report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: BFCL completion-suffix diagnostic report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
