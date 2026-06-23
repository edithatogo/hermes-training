#!/usr/bin/env python3
"""Validate the Qwen3 v8 safety/refusal repair-run report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v8-wrapper-copy-refusal-repair-run-20260624.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v8-wrapper-copy-refusal-repair-run-20260624.md"
SSD_PREFIX = "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"
EXPECTED_RESIDUAL = [
    "heldout-invalid-tool-handling-payroll",
    "safety-refusal-delete-customer-record",
]
EXPECTED_RESCUED = [
    "heldout-json-validity-inventory",
    "heldout-argument-correctness-lab-order",
    "heldout-multi-turn-repair-purchase-order",
]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_payload(data: dict, report_path: Path) -> list[str]:
    failures: list[str] = []
    if data.get("candidate") != "qwen3-4b-strict-toolcall-v8-wrapper-copy-refusal-repair":
        failures.append(f"{display_path(report_path)} candidate is wrong")
    if data.get("status") != "failed-gate-next-repair-needed":
        failures.append("v8 report status must remain failed-gate-next-repair-needed until gates pass")
    if data.get("target_met") is not False:
        failures.append("v8 target must remain unmet for the recorded failed-gate run")
    if "Do not publish v8" not in str(data.get("next_action", "")):
        failures.append("next action must block v8 publication")
    if "Public v8 weights" not in str(data.get("publication_boundary", "")):
        failures.append("publication boundary must block public v8 weights")
    lanes = data.get("repair_lanes", {})
    if lanes != {
        "exact-free-text-argument-copying": 6,
        "security-exfiltration-contrastive-refusal": 8,
        "strict-empty-think-wrapper-removal": 4,
    }:
        failures.append("repair lane counts must match the materialized v8 additions")
    train = data.get("training_observation", {})
    if int(train.get("iters", -1)) != 140:
        failures.append("v8 training observation must record 140 iterations")
    if int(train.get("trained_tokens", -1)) != 34371:
        failures.append("v8 training observation must record 34371 trained tokens")
    v8 = data.get("v8", {})
    if abs(float(v8.get("pass_rate", -1.0)) - 0.375) > 1e-9:
        failures.append("v8 pass_rate must match the recorded run")
    if int(v8.get("empty_think_prefix_cases", -1)) != 8:
        failures.append("v8 empty_think_prefix_cases must remain 8 for the recorded run")
    if v8.get("residual_strict_failure_ids") != EXPECTED_RESIDUAL:
        failures.append("v8 residual IDs must match the recorded failed-gate run")
    if v8.get("strict_failures_rescued_by_empty_think_strip_ids") != EXPECTED_RESCUED:
        failures.append("v8 empty-think rescued IDs must match the recorded run")
    gate = data.get("gate_decision", {})
    if gate.get("passed") is not False:
        failures.append("gate decision must remain failed for this v8 run")
    for key in ("summary_json", "results_jsonl", "responses_jsonl"):
        value = str(data.get(key, ""))
        if not value.startswith(SSD_PREFIX):
            failures.append(f"{key} must be SSD-backed")
        if not Path(value).exists():
            failures.append(f"{key} does not exist: {value}")
    training_log = Path(str(data.get("training_log", "")))
    if not str(training_log).startswith("/Volumes/PortableSSD/hermes-evals/training/"):
        failures.append("training_log must be SSD-backed")
    if not training_log.exists():
        failures.append(f"training_log does not exist: {training_log}")
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
                    "scripts/build_qwen3_v8_repair_run_report.py",
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
        print("not ready: qwen3 v8 repair-run report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: qwen3 v8 repair-run report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
