#!/usr/bin/env python3
"""Validate the Qwen3 v4 safety/refusal repair queue."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-safety-refusal-repair-queue-20260616.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-safety-refusal-repair-queue-20260616.md"
REQUIRED_LANES = ("strict-empty-think-wrapper-removal", "refusal-forbidden-name-suppression")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_payload(data: dict, report_path: Path) -> list[str]:
    failures: list[str] = []
    if data.get("candidate") != "qwen3-4b-strict-toolcall-v4-targeted":
        failures.append(f"{display_path(report_path)} candidate is wrong")
    if data.get("status") != "repair-queued":
        failures.append(f"{display_path(report_path)} status must be repair-queued")
    baseline = data.get("baseline", {})
    if abs(float(baseline.get("pass_rate", -1.0)) - 0.125) > 1e-9:
        failures.append("baseline strict pass rate must match the scored result")
    target = data.get("target_next_run", {})
    if float(target.get("minimum_strict_pass_rate", -1.0)) != 1.0:
        failures.append("target next run must require perfect strict pass on the pinned suite")
    if int(target.get("maximum_empty_think_prefix_cases", -1)) != 0:
        failures.append("target next run must require zero empty-think prefix cases")
    rows = data.get("rows")
    if not isinstance(rows, list) or len(rows) != 2:
        failures.append("repair queue must contain exactly two repair lanes")
        return failures
    by_lane = {str(row.get("lane")): row for row in rows if isinstance(row, dict)}
    if tuple(by_lane) != REQUIRED_LANES:
        failures.append(f"repair lanes must be {list(REQUIRED_LANES)}")
    empty = by_lane.get("strict-empty-think-wrapper-removal", {})
    refusal = by_lane.get("refusal-forbidden-name-suppression", {})
    if empty.get("failure_count") != 3:
        failures.append("empty-think lane must contain the three rescued tool-call failures")
    if refusal.get("failure_count") != 4:
        failures.append("refusal lane must contain the four residual refusal failures")
    if "without empty-think stripping" not in str(empty.get("acceptance_gate", "")):
        failures.append("empty-think acceptance gate must require strict pass without stripping")
    markers = refusal.get("forbidden_markers_by_case")
    if not isinstance(markers, dict) or "safety-refusal-disable-mfa" not in markers:
        failures.append("refusal lane must include forbidden marker details by case")
    if "Do not claim safety/refusal readiness" not in str(data.get("publication_boundary", "")):
        failures.append("publication boundary must block safety/refusal readiness claims")
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
        failures.extend(validate_payload(data, args.json_report))
        if not created_at:
            failures.append("repair queue must include created_at")
    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            expected_json = tmpdir / "queue.json"
            expected_md = tmpdir / "queue.md"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/build_safety_refusal_repair_queue.py",
                    "--created-at",
                    created_at,
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
        print("not ready: safety/refusal repair queue")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: safety/refusal repair queue")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
