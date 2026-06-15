#!/usr/bin/env python3
"""Validate downloaded Kaggle PEFT lm-eval scorecard artifacts before claims."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = Path("/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613/summary.json")
DEFAULT_JSON = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-result-ingest-20260614.json"
DEFAULT_MARKDOWN = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-result-ingest-20260614.md"
EXPECTED_TASKS = ("arc_challenge", "hellaswag", "truthfulqa_mc2", "gsm8k", "winogrande")
EXPECTED_ADAPTER_REPO = "edithatogo/qwen3-4b-hermes-lora-peft-converted"
EXPECTED_BASE_MODEL = "Qwen/Qwen3-4B"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def task_set(value: Any) -> set[str]:
    if isinstance(value, str):
        return {item.strip() for item in value.split(",") if item.strip()}
    if isinstance(value, list):
        return {str(item).strip() for item in value if str(item).strip()}
    return set()


def find_lm_eval_result(output_dir: Path) -> Path | None:
    candidates = [
        output_dir / "results.json",
        output_dir / "results.jsonl",
    ]
    candidates.extend(sorted(output_dir.glob("**/results*.json")))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def extract_result_tasks(result_path: Path | None) -> set[str]:
    if result_path is None or not result_path.exists() or result_path.suffix != ".json":
        return set()
    data = load_json(result_path)
    results = data.get("results")
    if isinstance(results, dict):
        return set(results)
    return set()


def resolve_recovered_output_dir(summary_json: Path, output_dir_value: Any) -> Path:
    output_dir = Path(str(output_dir_value or ""))
    if output_dir.is_absolute() and str(output_dir).startswith("/kaggle/working/"):
        recovered = summary_json.parent / output_dir.name
        if recovered.exists():
            return recovered
    if not output_dir.is_absolute():
        return summary_json.parent / output_dir
    return output_dir


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": passed, "detail": detail})


def validate_ingest(summary_json: Path, storage_root: Path, allow_pending: bool) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    if not summary_json.exists():
        add_check(
            checks,
            "summary_present",
            bool(allow_pending),
            f"pending artifact: {summary_json}" if allow_pending else f"missing: {summary_json}",
        )
        return {
            "status": "pending_artifacts" if allow_pending else "fail",
            "summary_json": str(summary_json),
            "storage_root": str(storage_root),
            "expected_tasks": list(EXPECTED_TASKS),
            "checks": checks,
            "claim_boundary": "No benchmark claim until a scored no-limit Kaggle summary and complete lm-eval results pass this validator.",
        }

    summary = load_json(summary_json)
    output_dir = resolve_recovered_output_dir(summary_json, summary.get("output_dir", ""))
    result_path = find_lm_eval_result(output_dir)
    found_tasks = extract_result_tasks(result_path)
    command = summary.get("evaluation", {}).get("command", [])
    command_text = " ".join(str(item) for item in command) if isinstance(command, list) else str(command)

    add_check(checks, "summary_on_storage_root", str(summary_json.resolve()).startswith(str(storage_root)), str(summary_json))
    add_check(checks, "status_scored", summary.get("status") == "scored", str(summary.get("status")))
    add_check(checks, "adapter_repo_expected", summary.get("adapter_repo") == EXPECTED_ADAPTER_REPO, str(summary.get("adapter_repo")))
    add_check(checks, "base_model_expected", summary.get("base_model") == EXPECTED_BASE_MODEL, str(summary.get("base_model")))
    add_check(checks, "configured_tasks_complete", task_set(summary.get("tasks")) == set(EXPECTED_TASKS), str(summary.get("tasks")))
    add_check(checks, "no_limit_configured", summary.get("limit") is None, str(summary.get("limit")))
    add_check(checks, "evaluation_returncode_zero", summary.get("evaluation", {}).get("returncode") == 0, str(summary.get("evaluation", {}).get("returncode")))
    add_check(checks, "evaluation_not_timed_out", summary.get("evaluation", {}).get("timed_out") is False, str(summary.get("evaluation", {}).get("timed_out")))
    add_check(checks, "command_has_no_limit_flag", "--limit" not in command_text, command_text[:240])
    add_check(checks, "output_dir_on_storage_root", str(output_dir.resolve()).startswith(str(storage_root)), str(output_dir))
    add_check(checks, "lm_eval_result_present", result_path is not None, str(result_path))
    add_check(checks, "lm_eval_tasks_complete", found_tasks == set(EXPECTED_TASKS), ",".join(sorted(found_tasks)) or "none")

    return {
        "status": "pass" if all(check["passed"] for check in checks) else "fail",
        "summary_json": str(summary_json),
        "storage_root": str(storage_root),
        "output_dir": str(output_dir),
        "lm_eval_result": str(result_path) if result_path else None,
        "expected_tasks": list(EXPECTED_TASKS),
        "found_tasks": sorted(found_tasks),
        "checks": checks,
        "claim_boundary": "No benchmark claim until a scored no-limit Kaggle summary and complete lm-eval results pass this validator.",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 V4 PEFT Kaggle Result Ingest Gate",
        "",
        f"Status: `{report['status']}`",
        f"Summary JSON: `{report['summary_json']}`",
        f"Storage root: `{report['storage_root']}`",
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
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--storage-root", type=Path, default=Path("/Volumes/PortableSSD"))
    parser.add_argument("--allow-pending", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    report = validate_ingest(args.summary_json, args.storage_root, args.allow_pending)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] in {"pass", "pending_artifacts"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
