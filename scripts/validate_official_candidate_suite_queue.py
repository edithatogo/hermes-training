#!/usr/bin/env python3
"""Validate the official-candidate benchmark execution queue."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.json"
REQUIRED_SUITES = ("official-bfcl", "official-coding", "safety-refusal", "ruler-long-context")
REQUIRED_STATUS = "blocked-missing-official-candidates"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path = DEFAULT_REPORT) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"]

    report = load(path)
    if report.get("candidate") != "qwen3-4b-strict-toolcall-v4-targeted":
        errors.append("candidate must be qwen3-4b-strict-toolcall-v4-targeted")
    if report.get("status") != REQUIRED_STATUS:
        errors.append(f"status must be {REQUIRED_STATUS}")

    items = report.get("items")
    if not isinstance(items, list):
        return errors + ["items must be a list"]

    by_suite = {str(item.get("suite")): item for item in items if isinstance(item, dict)}
    for suite in REQUIRED_SUITES:
        item = by_suite.get(suite)
        if not item:
            errors.append(f"missing suite {suite}")
            continue
        if item.get("status") != "missing":
            errors.append(f"{suite}: status must remain missing until scored evidence exists")
        if not str(item.get("run_id", "")).startswith("qwen3-v4-peft-"):
            errors.append(f"{suite}: run_id must be qwen3-v4-peft scoped")
        if "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/" not in str(item.get("output_root", "")):
            errors.append(f"{suite}: output_root must be SSD-backed standard-benchmarks")
        for key in ("blocker", "next_action", "local_command", "cloud_command", "publication_boundary"):
            if not str(item.get(key, "")).strip():
                errors.append(f"{suite}: missing {key}")
        criteria = item.get("completion_criteria")
        if not isinstance(criteria, list) or len(criteria) < 3:
            errors.append(f"{suite}: completion_criteria must contain at least three checks")
        if "No public broad benchmark claim" not in str(item.get("publication_boundary", "")):
            errors.append(f"{suite}: publication boundary must block broad claims")

    missing = report.get("missing_suites")
    if tuple(missing or ()) != REQUIRED_SUITES:
        errors.append(f"missing_suites must be {list(REQUIRED_SUITES)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    errors = validate(args.report)
    if errors:
        for error in errors:
            print(f"fail: {error}")
        return 1
    print("ok: official candidate suite queue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
