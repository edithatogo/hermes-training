#!/usr/bin/env python3
"""Validate the prompt/profile repair execution ledger is current."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STEM = ROOT / "reports/benchmark/coverage/prompt-profile-repair-ledger-20260614"
DEFAULT_JSON = DEFAULT_STEM.with_suffix(".json")
DEFAULT_MD = DEFAULT_STEM.with_suffix(".md")
EXPECTED_ROWS = 18


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def assert_same(expected: Path, actual: Path, failures: list[str]) -> None:
    if expected.read_text(encoding="utf-8") != actual.read_text(encoding="utf-8"):
        failures.append(f"{display_path(actual)} is stale; regenerate it")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-stem", type=Path, default=DEFAULT_STEM)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MD)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    for path in (args.json_report, args.markdown_report):
        if not path.exists():
            failures.append(f"missing {display_path(path)}")

    created_at = ""
    if not failures:
        data = json.loads(args.json_report.read_text(encoding="utf-8"))
        created_at = str(data.get("created_at") or "")
        rows = data.get("rows", [])
        if not isinstance(rows, list) or len(rows) != EXPECTED_ROWS:
            failures.append(f"{display_path(args.json_report)} must contain {EXPECTED_ROWS} rows")
        if not created_at:
            failures.append(f"{display_path(args.json_report)} has no created_at timestamp")
        statuses = {str(row.get("status", "")) for row in rows if isinstance(row, dict)}
        if "blocked-non-local" not in statuses:
            failures.append("ledger is missing status blocked-non-local")
        if "pending-endpoint" not in statuses and statuses != {"completed-no-promotion", "blocked-non-local"}:
            failures.append("ledger is missing status pending-endpoint")
        if "completed-no-promotion" not in statuses:
            failures.append("ledger is missing completed-no-promotion evidence")
        for row in rows if isinstance(rows, list) else []:
            label = str(row.get("candidate", "<unknown>"))
            if not row.get("promotion_gate"):
                failures.append(f"{label} has no promotion gate")
            if row.get("status") == "blocked-non-local" and row.get("experiments"):
                failures.append(f"{label} is blocked-non-local but has executable experiments")
            if row.get("status") != "blocked-non-local" and not row.get("experiments"):
                failures.append(f"{label} has no executable experiments")
            if str(row.get("status", "")).startswith("completed") and not row.get("result_report"):
                failures.append(f"{label} is completed but has no result_report")
            if row.get("result_report") and not (ROOT / str(row["result_report"])).exists():
                failures.append(f"{label} result_report does not exist: {row['result_report']}")
            result_reports = row.get("result_reports", [])
            if result_reports and not isinstance(result_reports, list):
                failures.append(f"{label} result_reports must be a list")
            if isinstance(result_reports, list):
                for result_report in result_reports:
                    if not (ROOT / str(result_report)).exists():
                        failures.append(f"{label} result_reports entry does not exist: {result_report}")

    if not failures:
        with tempfile.TemporaryDirectory() as tmp:
            output_stem = Path(tmp) / args.output_stem.name
            subprocess.run(
                [
                    sys.executable,
                    "scripts/build_prompt_profile_repair_ledger.py",
                    "--output-stem",
                    str(output_stem),
                    "--created-at",
                    created_at,
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            assert_same(output_stem.with_suffix(".json"), args.json_report, failures)
            assert_same(output_stem.with_suffix(".md"), args.markdown_report, failures)

    if failures:
        print("not ready: prompt/profile repair ledger")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: prompt/profile repair ledger is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
