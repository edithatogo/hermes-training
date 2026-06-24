#!/usr/bin/env python3
"""Validate the BFCL zero-score failure-analysis report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-bfcl-zero-score-failure-analysis-20260624.json"


def validate_report(path: Path = DEFAULT_REPORT) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"]
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("status") != "blocked-clean-regeneration-required":
        failures.append("BFCL failure analysis must remain blocked until clean regeneration exists")
    summary = report.get("summary", {})
    counts = summary.get("counts", {})
    if int(summary.get("total_rows", 0)) <= 0:
        failures.append("BFCL failure analysis must include result rows")
    if int(counts.get("upstream_error", 0)) <= 0:
        failures.append("BFCL failure analysis must record upstream endpoint errors from the stale artifact")
    if int(counts.get("blank_output", 0)) <= 0:
        failures.append("BFCL failure analysis must record blank outputs from the stale artifact")
    if report.get("gate", {}).get("promotable") is not False:
        failures.append("contaminated BFCL zero-score artifact must not be promotable")
    required_categories = {"multiple", "parallel", "simple_python"}
    categories = set(report.get("categories", {}))
    missing = sorted(required_categories - categories)
    if missing:
        failures.append(f"BFCL failure analysis missing categories: {missing}")
    contract = "\n".join(report.get("gate", {}).get("rerun_contract", []))
    for required in ("--num-threads 1", "--allow-overwrite", "upstream_error_rows == 0", "blank_output_rows == 0"):
        if required not in contract:
            failures.append(f"BFCL rerun contract missing {required!r}")
    md = path.with_suffix(".md")
    if not md.exists():
        failures.append(f"missing {md.relative_to(ROOT)}")
    elif "not promotable" not in md.read_text(encoding="utf-8"):
        failures.append("BFCL markdown report must state that the artifact is not promotable")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    failures = validate_report(args.report)
    if failures:
        print("not ready: BFCL zero-score failure analysis")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: BFCL zero-score failure analysis")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
