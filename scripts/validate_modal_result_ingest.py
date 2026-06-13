#!/usr/bin/env python3
"""Validate Modal PEFT lm-eval scorecard artifacts before benchmark claims."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULT = ROOT / "reports/cloud/modal-qwen3-v4-peft-scorecard-20260614/modal-result.json"
DEFAULT_JSON = ROOT / "reports/cloud/qwen3-v4-peft-modal-result-ingest-20260614.json"
DEFAULT_MARKDOWN = ROOT / "reports/cloud/qwen3-v4-peft-modal-result-ingest-20260614.md"
EXPECTED_TASKS = ("arc_challenge", "hellaswag", "truthfulqa_mc2", "gsm8k", "winogrande")
EXPECTED_ADAPTER_REPO = "edithatogo/qwen3-4b-hermes-lora-peft-converted"
EXPECTED_BASE_MODEL = "Qwen/Qwen3-4B"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_modal_payload(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if isinstance(data, str):
        parsed = json.loads(data)
    else:
        parsed = data
    if not isinstance(parsed, dict):
        raise ValueError(f"{path}: expected JSON object or JSON-encoded object string")
    return parsed


def task_set(value: Any) -> set[str]:
    if isinstance(value, str):
        return {item.strip() for item in value.split(",") if item.strip()}
    if isinstance(value, list):
        return {str(item).strip() for item in value if str(item).strip()}
    return set()


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": passed, "detail": detail})


def validate_ingest(result_json: Path, allow_pending: bool) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    if not result_json.exists():
        add_check(
            checks,
            "modal_result_present",
            bool(allow_pending),
            f"pending artifact: {result_json}" if allow_pending else f"missing: {result_json}",
        )
        return {
            "status": "pending_artifacts" if allow_pending else "fail",
            "result_json": str(result_json),
            "expected_tasks": list(EXPECTED_TASKS),
            "checks": checks,
            "claim_boundary": "No benchmark claim until Modal returns a scored no-limit summary with complete lm-eval task results.",
        }

    summary = parse_modal_payload(result_json)
    command = summary.get("evaluation", {}).get("command", [])
    command_text = " ".join(str(item) for item in command) if isinstance(command, list) else str(command)
    result_files = summary.get("result_files", [])
    found_tasks: set[str] = set()
    if isinstance(result_files, list):
        for file_name in result_files:
            text = str(file_name)
            for task in EXPECTED_TASKS:
                if task in text:
                    found_tasks.add(task)

    add_check(checks, "status_scored", summary.get("status") == "scored", str(summary.get("status")))
    add_check(checks, "adapter_repo_expected", summary.get("adapter_repo") == EXPECTED_ADAPTER_REPO, str(summary.get("adapter_repo")))
    add_check(checks, "base_model_expected", summary.get("base_model") == EXPECTED_BASE_MODEL, str(summary.get("base_model")))
    add_check(checks, "configured_tasks_complete", task_set(summary.get("tasks")) == set(EXPECTED_TASKS), str(summary.get("tasks")))
    add_check(checks, "no_limit_configured", summary.get("limit") is None, str(summary.get("limit")))
    add_check(checks, "evaluation_returncode_zero", summary.get("evaluation", {}).get("returncode") == 0, str(summary.get("evaluation", {}).get("returncode")))
    add_check(checks, "evaluation_not_timed_out", summary.get("evaluation", {}).get("timed_out") is False, str(summary.get("evaluation", {}).get("timed_out")))
    add_check(checks, "command_has_no_limit_flag", "--limit" not in command_text, command_text[:240])
    add_check(checks, "result_files_present", bool(result_files), str(result_files[:5] if isinstance(result_files, list) else result_files))
    add_check(checks, "lm_eval_tasks_recoverable", found_tasks == set(EXPECTED_TASKS), ",".join(sorted(found_tasks)) or "none")

    return {
        "status": "pass" if all(check["passed"] for check in checks) else "fail",
        "result_json": str(result_json),
        "expected_tasks": list(EXPECTED_TASKS),
        "found_tasks": sorted(found_tasks),
        "checks": checks,
        "claim_boundary": "No benchmark claim until Modal returns a scored no-limit summary with complete lm-eval task results.",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 V4 PEFT Modal Result Ingest Gate",
        "",
        f"Status: `{report['status']}`",
        f"Result JSON: `{report['result_json']}`",
        "",
        "## Claim Boundary",
        "",
        report["claim_boundary"],
        "",
        "## Expected Complete Tasks",
        "",
        ", ".join(f"`{task}`" for task in report["expected_tasks"]),
        "",
        "## Checks",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    for check in report["checks"]:
        result = "pass" if check["passed"] else "fail"
        lines.append(f"| `{check['name']}` | `{result}` | {check['detail']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result-json", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--allow-pending", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    report = validate_ingest(args.result_json, args.allow_pending)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] in {"pass", "pending_artifacts"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
