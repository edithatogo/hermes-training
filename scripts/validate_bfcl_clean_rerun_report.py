#!/usr/bin/env python3
"""Validate the Qwen3 v4 BFCL clean-rerun report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-bfcl-clean-rerun-20260624.json"
SSD_PREFIX = "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/"


def validate_report(path: Path = DEFAULT_REPORT) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"]
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("status") != "blocked-blank-output-gate":
        failures.append("clean BFCL rerun must remain blocked on blank-output gate until a passing rerun exists")
    run_root = str(report.get("run_root", ""))
    if not run_root.startswith(SSD_PREFIX):
        failures.append("BFCL clean rerun root must be SSD-backed")
    summary = report.get("summary", {})
    if int(summary.get("total_rows", 0)) <= 0:
        failures.append("BFCL clean rerun report must include generated rows")
    if int(summary.get("upstream_error_rows", -1)) != 0:
        failures.append("BFCL clean rerun should have cleared upstream errors")
    if int(summary.get("blank_output_rows", 0)) <= 0:
        failures.append("BFCL clean rerun must record the blank-output blocker")
    if report.get("gate", {}).get("passed") is not False:
        failures.append("blank-output BFCL rerun must not pass the gate")
    categories = set(report.get("categories", {}))
    if "multiple" not in categories:
        failures.append("BFCL clean rerun must include at least the generated multiple category")
    logs = report.get("logs", {})
    for key in ("mlx_server", "proxy", "generate", "evaluate"):
        value = Path(str(logs.get(key, "")))
        if not value.exists():
            failures.append(f"missing BFCL clean rerun log {key}: {value}")
    md = path.with_suffix(".md")
    if not md.exists():
        failures.append(f"missing {md.relative_to(ROOT)}")
    elif "blocked-blank-output-gate" not in md.read_text(encoding="utf-8"):
        failures.append("BFCL clean rerun markdown must record the blank-output gate")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    failures = validate_report(args.report)
    if failures:
        print("not ready: BFCL clean rerun report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: BFCL clean rerun report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
