#!/usr/bin/env python3
"""Validate tracked prompt/profile repair result reports."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT / "reports/benchmark/coverage/prompt-profile-repair-results-20260614.json"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def validate_results(path: Path = DEFAULT_RESULTS) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"]
    data = load_json(path)
    results = data.get("results", [])
    if not isinstance(results, list) or not results:
        return [f"{path.relative_to(ROOT)} must contain non-empty results"]
    for result in results:
        if not isinstance(result, dict):
            failures.append("result entries must be objects")
            continue
        label = f"{result.get('candidate', '<unknown>')}:{result.get('variant', '<unknown>')}"
        report = ROOT / str(result.get("result_report", ""))
        source_summary = Path(str(result.get("source_summary", "")))
        if result.get("status") != "completed-no-promotion":
            failures.append(f"{label} has unsupported status {result.get('status')!r}")
        if float(result.get("pass_rate", -1)) != 0.0:
            failures.append(f"{label} expected pass_rate 0.0 for tracked failed repair")
        if int(result.get("cases", 0)) != 3:
            failures.append(f"{label} expected 3 cases")
        if int(result.get("passed", -1)) != 0:
            failures.append(f"{label} expected 0 passed")
        if not report.exists():
            failures.append(f"{label} missing result report {report}")
        if not source_summary.exists():
            failures.append(f"{label} missing source summary {source_summary}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-json", type=Path, default=DEFAULT_RESULTS)
    args = parser.parse_args()

    failures = validate_results(args.results_json)
    if failures:
        print("not ready: prompt/profile repair results")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: prompt/profile repair results are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
