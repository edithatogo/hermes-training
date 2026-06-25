#!/usr/bin/env python3
"""Validate the official-candidate execution matrix."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-execution-matrix-20260616.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-execution-matrix-20260616.md"
REQUIRED_SUITES = ("official-bfcl", "official-coding", "safety-refusal", "ruler-long-context")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_payload(data: dict, report_path: Path) -> list[str]:
    failures: list[str] = []
    if data.get("candidate") != "qwen3-4b-strict-toolcall-v4-targeted":
        failures.append(f"{display_path(report_path)} candidate is wrong")
    if data.get("status") not in {
        "blocked-pending-scored-artifacts",
        "scored-artifacts-present-repair-required",
    }:
        failures.append(f"{display_path(report_path)} status is invalid")
    rows = data.get("rows")
    if not isinstance(rows, list):
        return failures + [f"{display_path(report_path)} rows must be a list"]
    by_suite = {str(row.get("suite")): row for row in rows if isinstance(row, dict)}
    if tuple(by_suite) != REQUIRED_SUITES:
        failures.append(f"{display_path(report_path)} suites must be {list(REQUIRED_SUITES)}")
    for suite in REQUIRED_SUITES:
        row = by_suite.get(suite)
        if not row:
            continue
        if row.get("queue_status") != "missing":
            failures.append(f"{suite}: queue_status must remain missing until scored evidence exists")
        if row.get("execution_status") not in {
            "blocked-preflight",
            "blocked-runtime",
            "ready-for-runtime",
            "scored-artifact-present",
        }:
            failures.append(f"{suite}: invalid execution_status {row.get('execution_status')!r}")
        if not str(row.get("output_root", "")).startswith("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/"):
            failures.append(f"{suite}: output_root must be SSD-backed")
        if not str(row.get("completion_artifact", "")).startswith("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/"):
            failures.append(f"{suite}: completion_artifact must be SSD-backed")
        if not str(row.get("local_command", "")).strip():
            failures.append(f"{suite}: local_command is missing")
    if by_suite.get("official-bfcl", {}).get("execution_status") not in {"blocked-preflight", "ready-for-runtime", "scored-artifact-present"}:
        failures.append("official-bfcl should remain blocked, ready, or scored when BFCL artifacts exist")
    if by_suite.get("official-coding", {}).get("execution_status") not in {
        "blocked-preflight",
        "blocked-runtime",
        "scored-artifact-present",
    }:
        failures.append("official-coding should remain blocked until generated solutions exist or scored after EvalPlus")
    if by_suite.get("safety-refusal", {}).get("execution_status") != "scored-artifact-present":
        failures.append("safety-refusal should record the scored artifact after local runtime completion")
    if by_suite.get("ruler-long-context", {}).get("execution_status") not in {
        "blocked-preflight",
        "blocked-runtime",
        "ready-for-runtime",
        "scored-artifact-present",
    }:
        failures.append("ruler-long-context should be blocked, ready, or scored when RULER artifacts exist")
    if "No public broad benchmark claim" not in str(data.get("publication_boundary", "")):
        failures.append("publication boundary must block broad claims")
    if data.get("status") == "scored-artifacts-present-repair-required":
        if any(row.get("execution_status") != "scored-artifact-present" for row in rows if isinstance(row, dict)):
            failures.append("repair-required status requires scored artifacts for every suite")
    bridge = data.get("latest_bfcl_bridge_smoke")
    if not isinstance(bridge, dict):
        failures.append("latest_bfcl_bridge_smoke is missing")
    else:
        scores = bridge.get("scores", {})
        if abs(float(scores.get("overall_acc", -1.0)) - 0.0033) > 0.0001:
            failures.append("latest BFCL bridge smoke overall_acc must be 0.0033")
        if abs(float(scores.get("simple_python_ast", -1.0)) - 0.1) > 0.0001:
            failures.append("latest BFCL bridge smoke simple_python_ast must be 0.1")
        if abs(float(scores.get("multiple_ast", -1.0)) - 0.1) > 0.0001:
            failures.append("latest BFCL bridge smoke multiple_ast must be 0.1")
        if abs(float(scores.get("parallel_ast", -1.0)) - 0.0) > 0.0001:
            failures.append("latest BFCL bridge smoke parallel_ast must be 0.0")
        if bridge.get("bfcl_claim_allowed") is not False:
            failures.append("latest BFCL bridge smoke must keep BFCL claims blocked")
        if not str(bridge.get("run_root", "")).startswith("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/"):
            failures.append("latest BFCL bridge smoke run_root must be SSD-backed")
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
            expected_json = tmpdir / "matrix.json"
            expected_md = tmpdir / "matrix.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/build_official_candidate_execution_matrix.py",
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
        print("not ready: official-candidate execution matrix")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: official-candidate execution matrix")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
