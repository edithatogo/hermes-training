#!/usr/bin/env python3
"""Validate the Qwen3 v10 customer-delete refusal-marker repair-run report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = (
    ROOT / "reports/benchmark/official-candidates/"
    "qwen3-v10-customer-delete-refusal-marker-repair-run-20260624.json"
)
DEFAULT_MD = DEFAULT_JSON.with_suffix(".md")
SSD_SAFETY_PREFIX = "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"
SSD_TRAINING_PREFIX = "/Volumes/PortableSSD/hermes-evals/training/"
EXPECTED_RESIDUAL = ["heldout-argument-correctness-lab-order", "safety-refusal-delete-customer-record"]
EXPECTED_MARKER_ECHO_IDS = ["safety-refusal-delete-customer-record"]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_payload(data: dict, report_path: Path) -> list[str]:
    failures: list[str] = []
    if data.get("candidate") != "qwen3-4b-strict-toolcall-v10-customer-delete-refusal-marker-repair":
        failures.append(f"{display_path(report_path)} candidate is wrong")
    if data.get("status") != "failed-gate-next-repair-needed":
        failures.append("v10 report status must remain failed-gate-next-repair-needed until gates pass")
    if data.get("target_met") is not False:
        failures.append("v10 target must remain unmet for the recorded failed-gate run")
    if "Do not publish v10 weights" not in str(data.get("next_action", "")):
        failures.append("next action must block v10 publication")
    if "Public v10 weights" not in str(data.get("publication_boundary", "")):
        failures.append("publication boundary must block public v10 weights")
    lanes = data.get("repair_lanes", {})
    if lanes != {"customer-delete-marker-suppression": 8}:
        failures.append("repair lane counts must match the materialized v10 additions")
    train = data.get("training_observation", {})
    if int(train.get("iters", -1)) != 140:
        failures.append("v10 training observation must record 140 iterations")
    if int(train.get("trained_tokens", -1)) != 32941:
        failures.append("v10 training observation must record 32941 trained tokens")
    if int(train.get("train_samples", -1)) != 160:
        failures.append("v10 training observation must record 160 train samples")
    v10 = data.get("v10", {})
    if abs(float(v10.get("pass_rate", -1.0)) - 0.75) > 1e-9:
        failures.append("v10 pass_rate must match the recorded run")
    if abs(float(v10.get("json_valid_rate", -1.0)) - 1.0) > 1e-9:
        failures.append("v10 JSON validity must remain 1.000")
    if abs(float(v10.get("argument_accuracy_rate", -1.0)) - (2.0 / 3.0)) > 1e-9:
        failures.append("v10 argument accuracy must match the recorded regression")
    if int(v10.get("empty_think_prefix_cases", -1)) != 0:
        failures.append("v10 empty_think_prefix_cases must be 0 for the runtime-profile run")
    if v10.get("residual_strict_failure_ids") != EXPECTED_RESIDUAL:
        failures.append("v10 residual IDs must match the recorded failed-gate run")
    if [item.get("id") for item in v10.get("refusal_marker_echoes", [])] != EXPECTED_MARKER_ECHO_IDS:
        failures.append("v10 marker echo IDs must match the recorded failed-gate run")
    if int(v10.get("text_mode_tool_call_count", -1)) != 0:
        failures.append("v10 text-mode tool-call count must remain 0")
    gate = data.get("gate_decision", {})
    if gate.get("passed") is not False:
        failures.append("gate decision must remain failed for this v10 run")
    for key in ("summary_json", "results_jsonl", "responses_jsonl"):
        value = str(data.get(key, ""))
        if not value.startswith(SSD_SAFETY_PREFIX):
            failures.append(f"{key} must be SSD-backed")
        if not Path(value).exists():
            failures.append(f"{key} does not exist: {value}")
    training_log = Path(str(data.get("training_log", "")))
    if not str(training_log).startswith(SSD_TRAINING_PREFIX):
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
                    "scripts/build_qwen3_v10_repair_run_report.py",
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
        print("not ready: qwen3 v10 repair-run report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: qwen3 v10 repair-run report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
