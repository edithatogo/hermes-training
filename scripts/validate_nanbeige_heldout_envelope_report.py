#!/usr/bin/env python3
"""Validate the tracked Nanbeige held-out constrained-envelope report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/constrained-envelope/nanbeige41-3b-heldout-constrained-envelope-20260614.json"
DEFAULT_MD = ROOT / "reports/benchmark/constrained-envelope/nanbeige41-3b-heldout-constrained-envelope-20260614.md"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def validate_report(path: Path = DEFAULT_JSON, markdown_path: Path = DEFAULT_MD) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"]
    if not markdown_path.exists():
        failures.append(f"missing {markdown_path.relative_to(ROOT)}")
    data = load_json(path)
    if data.get("model") != "Nanbeige/Nanbeige4.1-3B":
        failures.append("held-out diagnostic must target Nanbeige/Nanbeige4.1-3B")
    if data.get("suite") != "benchmarks/tool_call_local/heldout_suite.json":
        failures.append("held-out diagnostic must use benchmarks/tool_call_local/heldout_suite.json")
    if data.get("promotion_allowed") is not False:
        failures.append("held-out diagnostic must explicitly set promotion_allowed false")
    if int(data.get("cases", 0)) != 8:
        failures.append("held-out diagnostic must contain eight cases")
    if float(data.get("raw_pass_rate", -1)) != 0.125:
        failures.append("held-out diagnostic must preserve the raw strict 1/8 baseline")
    if float(data.get("constrained_pass_rate", -1)) != 0.375:
        failures.append("held-out diagnostic must record the constrained 3/8 result")
    if float(data.get("constrained_pass_rate", 0)) >= 1.0:
        failures.append("held-out diagnostic must not be represented as a pass")
    if "not raw-output promotion" not in str(data.get("claim_boundary", "")):
        failures.append("held-out diagnostic must state that envelope evidence is not raw-output promotion")

    for key in ("source_output_dir", "source_summary", "output_dir"):
        source = Path(str(data.get(key, "")))
        if not source.exists():
            failures.append(f"missing {key} {source}")
    output_dir = Path(str(data.get("output_dir", "")))
    for name in ("summary.json", "summary.md", "responses.jsonl", "results.jsonl"):
        if not (output_dir / name).exists():
            failures.append(f"missing held-out diagnostic output {output_dir / name}")

    cases = data.get("case_results", [])
    if not isinstance(cases, list) or len(cases) != 8:
        failures.append("held-out diagnostic must contain eight case results")
    else:
        passed = [row for row in cases if isinstance(row, dict) and row.get("pass")]
        failed = [row for row in cases if isinstance(row, dict) and not row.get("pass")]
        if len(passed) != 3 or len(failed) != 5:
            failures.append("held-out diagnostic must preserve the 3 pass / 5 fail case split")
        actions = {str(row.get("envelope_action", "")) for row in cases if isinstance(row, dict)}
        if "selected-tool-calls" not in actions:
            failures.append("held-out diagnostic must include selected-tool-calls evidence")
        if "selected-refusal-sentence" not in actions:
            failures.append("held-out diagnostic must include selected-refusal-sentence evidence")
        if "stripped-thinking-only" not in actions:
            failures.append("held-out diagnostic must include residual stripped-thinking failures")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--report-md", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    failures = validate_report(args.report_json, args.report_md)
    if failures:
        print("not ready: Nanbeige held-out constrained-envelope report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: Nanbeige held-out constrained-envelope report is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
