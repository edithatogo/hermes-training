#!/usr/bin/env python3
"""Validate the constrained-envelope repair plan."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/benchmark/coverage/constrained-envelope-repair-plan-20260614.json"
DEFAULT_MD = ROOT / "reports/benchmark/coverage/constrained-envelope-repair-plan-20260614.md"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def validate_plan(path: Path = DEFAULT_JSON, markdown_path: Path = DEFAULT_MD) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"]
    if not markdown_path.exists():
        failures.append(f"missing {markdown_path.relative_to(ROOT)}")
    data = load_json(path)
    candidates = data.get("candidates")
    if data.get("promotion_allowed") is not False:
        failures.append("plan must explicitly set promotion_allowed false")
    if not isinstance(candidates, list) or not candidates:
        failures.append("plan must contain ranked candidates")
        return failures

    high_priority = [row for row in candidates if row.get("priority") == "high"]
    if not high_priority:
        failures.append("plan must include at least one high-priority constrained-envelope candidate")
    top = candidates[0]
    top_metrics = top.get("case_metrics", {})
    if not isinstance(top_metrics, dict) or int(top_metrics.get("matched_tool_calls_extra_text", 0)) <= 0:
        failures.append("top candidate must have exact Hermes calls rejected only for extra text")
    if top.get("candidate") != "Nanbeige/Nanbeige4.1-3B":
        failures.append("Nanbeige/Nanbeige4.1-3B should remain the top constrained-envelope candidate")

    for row in candidates:
        label = str(row.get("candidate", "<unknown>"))
        boundary = str(row.get("promotion_boundary", ""))
        command = str(row.get("diagnostic_command", ""))
        if "No promotion" not in boundary:
            failures.append(f"{label} missing non-promotion boundary")
        if "--require-no-extra-tool-text" not in command:
            failures.append(f"{label} diagnostic command must preserve strict no-extra-text scoring")
        if "--run-id '" in command:
            failures.append(f"{label} diagnostic command must allow RUN_STAMP expansion in run id")
        if "run_endpoint_pilot_benchmark.py" in command and f"--model '{label}'" not in command:
            failures.append(f"{label} endpoint diagnostic command must use the candidate model id")
        if any(term in command for term in ("az ", "hf jobs", "modal run", "kaggle kernels", "lightning ")):
            failures.append(f"{label} diagnostic command must not launch cloud jobs")
        if "execute=true" in command.lower():
            failures.append(f"{label} diagnostic command must not contain execute=true")
        variants = row.get("variants", [])
        if not isinstance(variants, list) or not variants:
            failures.append(f"{label} must include source variants")
            continue
        for variant in variants:
            if not isinstance(variant, dict):
                failures.append(f"{label} variants must be objects")
                continue
            report = ROOT / str(variant.get("result_report", ""))
            source = variant.get("source", {})
            if not report.exists():
                failures.append(f"{label} missing result report {report}")
            if not isinstance(source, dict):
                failures.append(f"{label} source must be an object")
                continue
            for key in ("summary", "results", "responses"):
                source_path = Path(str(source.get(key, "")))
                if not source_path.exists():
                    failures.append(f"{label} missing source {key} {source_path}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--plan-md", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    failures = validate_plan(args.plan_json, args.plan_md)
    if failures:
        print("not ready: constrained-envelope repair plan")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: constrained-envelope repair plan is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
