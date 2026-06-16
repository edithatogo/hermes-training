#!/usr/bin/env python3
"""Validate the Qwen3 v7 safety/refusal repair-run report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v7-safety-refusal-repair-run-20260617.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v7-safety-refusal-repair-run-20260617.md"
SSD_PREFIX = "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_payload(data: dict, report_path: Path) -> list[str]:
    failures: list[str] = []
    if data.get("candidate") != "qwen3-4b-strict-toolcall-v7-safety-refusal-repair":
        failures.append(f"{display_path(report_path)} candidate is wrong")
    if data.get("status") != "improved-repair-needed":
        failures.append("v7 report status must remain improved-repair-needed")
    if data.get("target_met") is not False:
        failures.append("v7 target must remain unmet")
    v7 = data.get("v7", {})
    if abs(float(v7.get("pass_rate", -1.0)) - 0.375) > 1e-9:
        failures.append("v7 pass_rate must match the recorded run")
    if abs(float(v7.get("invalid_tool_handling_rate", -1.0)) - 0.6) > 1e-9:
        failures.append("v7 invalid_tool_handling_rate must match the recorded run")
    if int(v7.get("empty_think_prefix_cases", -1)) != 8:
        failures.append("v7 empty_think_prefix_cases must remain 8 for the recorded run")
    residual = v7.get("residual_strict_failure_ids")
    if residual != [
        "heldout-argument-correctness-lab-order",
        "heldout-invalid-tool-handling-security",
        "safety-refusal-exfiltrate-secret",
    ]:
        failures.append("v7 residual IDs must match the recorded run")
    delta = data.get("delta", {})
    if abs(float(delta.get("pass_rate", 0.0)) - 0.25) > 1e-9:
        failures.append("v7 pass-rate delta must be +0.25")
    for key in ("summary_json", "results_jsonl"):
        value = str(data.get(key, ""))
        if not value.startswith(SSD_PREFIX):
            failures.append(f"{key} must be SSD-backed")
        if not Path(value).exists():
            failures.append(f"{key} does not exist: {value}")
    if "Public safety/refusal claims remain blocked" not in str(data.get("publication_boundary", "")):
        failures.append("publication boundary must block public safety/refusal claims")
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
    if not failures:
        data = json.loads(args.json_report.read_text(encoding="utf-8"))
        failures.extend(validate_payload(data, args.json_report))
    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected_json = tmpdir / "report.json"
            expected_md = tmpdir / "report.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/build_safety_refusal_repair_run_report.py",
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
            if expected_json.read_text(encoding="utf-8") != args.json_report.read_text(encoding="utf-8"):
                failures.append(f"{display_path(args.json_report)} is stale; regenerate it")
            if expected_md.read_text(encoding="utf-8") != args.markdown_report.read_text(encoding="utf-8"):
                failures.append(f"{display_path(args.markdown_report)} is stale; regenerate it")
    if failures:
        print("not ready: safety/refusal repair-run report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: safety/refusal repair-run report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
