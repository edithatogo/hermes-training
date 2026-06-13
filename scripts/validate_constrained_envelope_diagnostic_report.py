#!/usr/bin/env python3
"""Validate the tracked Nanbeige constrained-envelope diagnostic report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/constrained-envelope/nanbeige41-3b-constrained-envelope-diagnostic-20260614.json"
DEFAULT_MD = ROOT / "reports/benchmark/constrained-envelope/nanbeige41-3b-constrained-envelope-diagnostic-20260614.md"


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
        failures.append("diagnostic must target Nanbeige/Nanbeige4.1-3B")
    if data.get("promotion_allowed") is not False:
        failures.append("diagnostic must explicitly set promotion_allowed false")
    if float(data.get("raw_pass_rate", -1)) != 0.0:
        failures.append("diagnostic must preserve the raw strict failure baseline")
    if float(data.get("constrained_pass_rate", -1)) < 1.0:
        failures.append("diagnostic envelope should pass the 3-case replay before follow-on work")
    if "not raw-output promotion" not in str(data.get("claim_boundary", "")):
        failures.append("diagnostic must state that envelope evidence is not raw-output promotion")
    for key in ("source_output_dir", "source_summary", "output_dir"):
        source = Path(str(data.get(key, "")))
        if not source.exists():
            failures.append(f"missing {key} {source}")
    output_dir = Path(str(data.get("output_dir", "")))
    for name in ("summary.json", "summary.md", "responses.jsonl", "results.jsonl"):
        if not (output_dir / name).exists():
            failures.append(f"missing diagnostic output {output_dir / name}")
    cases = data.get("case_results", [])
    if not isinstance(cases, list) or len(cases) != 3:
        failures.append("diagnostic must contain three case results")
    else:
        actions = {str(row.get("envelope_action", "")) for row in cases if isinstance(row, dict)}
        if "selected-tool-calls" not in actions:
            failures.append("diagnostic must include selected-tool-calls evidence")
        if "selected-refusal-sentence" not in actions:
            failures.append("diagnostic must include selected-refusal-sentence evidence")
        if any(not row.get("pass") for row in cases if isinstance(row, dict)):
            failures.append("all diagnostic replay cases should pass")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--report-md", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    failures = validate_report(args.report_json, args.report_md)
    if failures:
        print("not ready: constrained-envelope diagnostic report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: constrained-envelope diagnostic report is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
