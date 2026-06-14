#!/usr/bin/env python3
"""Validate generated cloud operator gate reports."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHECKLIST = ROOT / "reports/cloud/backend-unblock-checklist-20260613.json"
DEFAULT_JSON = ROOT / "reports/cloud/cloud-operator-gates-20260614.json"
DEFAULT_MARKDOWN = ROOT / "reports/cloud/cloud-operator-gates-20260614.md"
REQUIRED_BACKENDS = {"colab", "hf_jobs", "azure", "ngc", "kaggle", "modal", "lightning"}
SECRET_TERMS = ("token", "secret", "payment", "card")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate_semantics(report: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    rows = report.get("rows", [])
    if report.get("execution_allowed") is not False:
        failures.append("top-level execution_allowed must be false")
    if report.get("promotion_allowed") is not False:
        failures.append("top-level promotion_allowed must be false")
    if not isinstance(rows, list) or not rows:
        failures.append("rows must be a non-empty list")
        return failures
    backends = {row.get("backend") for row in rows if isinstance(row, dict)}
    missing = sorted(REQUIRED_BACKENDS - backends)
    if missing:
        failures.append(f"missing backend gates: {', '.join(missing)}")
    for row in rows:
        if not isinstance(row, dict):
            failures.append(f"invalid row: {row!r}")
            continue
        backend = row.get("backend", "<unknown>")
        if row.get("execution_allowed") is not False:
            failures.append(f"{backend}: execution_allowed must be false")
        if row.get("promotion_allowed") is not False:
            failures.append(f"{backend}: promotion_allowed must be false")
        evidence = row.get("external_evidence_required")
        if not isinstance(evidence, list) or not evidence:
            failures.append(f"{backend}: external evidence list is required")
        secret_policy = str(row.get("secret_policy", "")).lower()
        for term in SECRET_TERMS:
            if term not in secret_policy:
                failures.append(f"{backend}: secret policy must mention {term}")
    return failures


def assert_current(checklist: Path, json_path: Path, markdown_path: Path, failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        expected_json = Path(tmp) / "cloud-operator-gates.json"
        expected_md = Path(tmp) / "cloud-operator-gates.md"
        subprocess.run(
            [
                sys.executable,
                "scripts/build_cloud_operator_gates.py",
                "--checklist",
                relative(checklist),
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
        if expected_json.read_text(encoding="utf-8") != json_path.read_text(encoding="utf-8"):
            failures.append(f"{relative(json_path)} is stale")
        if expected_md.read_text(encoding="utf-8") != markdown_path.read_text(encoding="utf-8"):
            failures.append(f"{relative(markdown_path)} is stale")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    failures: list[str] = []
    for path in (args.checklist, args.json_report, args.markdown_report):
        if not path.exists():
            failures.append(f"missing {relative(path)}")
    if not failures:
        failures.extend(validate_semantics(load_json(args.json_report)))
        assert_current(args.checklist, args.json_report, args.markdown_report, failures)
    if failures:
        print("not ready: cloud operator gates")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: cloud operator gates are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
