#!/usr/bin/env python3
"""Validate the compact Qwen3 v4 safety/refusal result report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-safety-refusal-result-20260616.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-safety-refusal-result-20260616.md"
SUMMARY = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"
    "qwen3-v4-peft-safety-refusal-20260616/summary.json"
)
SSD_PREFIX = "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_payload(data: dict, report_path: Path) -> list[str]:
    failures: list[str] = []
    if data.get("candidate") != "qwen3-4b-strict-toolcall-v4-targeted":
        failures.append(f"{display_path(report_path)} candidate is wrong")
    if data.get("status") != "scored-repair-needed":
        failures.append(f"{display_path(report_path)} status must be scored-repair-needed")
    if data.get("cases") != 8:
        failures.append("safety/refusal report must contain 8 cases")
    if data.get("passed") != 1:
        failures.append("safety/refusal strict passed count must be 1 for the recorded run")
    if abs(float(data.get("pass_rate", -1.0)) - 0.125) > 1e-9:
        failures.append("safety/refusal pass_rate must match the recorded strict score")
    if abs(float(data.get("invalid_tool_handling_rate", -1.0)) - 0.2) > 1e-9:
        failures.append("safety/refusal invalid_tool_handling_rate must match the recorded score")
    for key in ("summary_json", "results_jsonl", "responses_jsonl"):
        value = str(data.get(key, ""))
        if not value.startswith(SSD_PREFIX):
            failures.append(f"{key} must be SSD-backed")
        if key == "summary_json" and not Path(value).exists():
            failures.append(f"{key} does not exist: {value}")
    if "Do not claim standardized safety/refusal" not in str(data.get("publication_boundary", "")):
        failures.append("publication boundary must block standardized safety/refusal claims")
    if "empty-think" not in str(data.get("next_action", "")):
        failures.append("next_action must call out empty-think wrapper repair")
    residual = data.get("residual_strict_failure_ids")
    if not isinstance(residual, list) or len(residual) != 4:
        failures.append("residual strict failure IDs must list the four remaining failures")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()
    failures: list[str] = []
    for path in (SUMMARY, args.json_report, args.markdown_report):
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
                    "scripts/build_safety_refusal_result_report.py",
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
        print("not ready: safety/refusal result report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: safety/refusal result report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
