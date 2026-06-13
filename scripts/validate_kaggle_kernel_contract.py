#!/usr/bin/env python3
"""Validate the staged Kaggle PEFT scorecard notebook contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STAGING_DIR = ROOT / "reports/cloud/kaggle-qwen3-v4-peft-scorecard-20260613"
DEFAULT_DRY_RUN = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-submit-dry-run-20260613.json"
DEFAULT_PREFLIGHT = ROOT / "reports/cloud/backend-preflight-20260613.json"
DEFAULT_JSON = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.json"
DEFAULT_MARKDOWN = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.md"
EXPECTED_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"
EXPECTED_ADAPTER_REPO = "edithatogo/qwen3-4b-hermes-lora-peft-converted"
EXPECTED_KERNEL_ID = "edithatogo/qwen3-v4-peft-lm-eval-selected-full"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": passed, "detail": detail})


def validate_contract(staging_dir: Path, dry_run_path: Path, preflight_path: Path) -> dict[str, Any]:
    metadata_path = staging_dir / "kernel-metadata.json"
    config_path = staging_dir / "kaggle-peft-lm-eval-config.json"
    runner_path = staging_dir / "kaggle_peft_lm_eval_selected.py"
    checks: list[dict[str, Any]] = []

    metadata = load_json(metadata_path)
    config = load_json(config_path)
    dry_run = load_json(dry_run_path)
    preflight = load_json(preflight_path)
    runner_text = runner_path.read_text(encoding="utf-8")
    kaggle_status = preflight.get("backends", {}).get("kaggle", {}).get("status")
    quota_probe = preflight.get("backends", {}).get("kaggle", {}).get("quota_sdk_probe", {})

    add_check(checks, "metadata_kernel_id", metadata.get("id") == EXPECTED_KERNEL_ID, str(metadata.get("id")))
    add_check(checks, "metadata_script_kernel", metadata.get("kernel_type") == "script", str(metadata.get("kernel_type")))
    add_check(checks, "metadata_python", metadata.get("language") == "python", str(metadata.get("language")))
    add_check(checks, "metadata_gpu_enabled", metadata.get("enable_gpu") is True, str(metadata.get("enable_gpu")))
    add_check(checks, "metadata_internet_enabled", metadata.get("enable_internet") is True, str(metadata.get("enable_internet")))
    add_check(checks, "metadata_public_kernel", metadata.get("is_private") is False, str(metadata.get("is_private")))
    add_check(checks, "metadata_license", metadata.get("license") == "apache-2.0", str(metadata.get("license")))
    add_check(checks, "config_adapter_public_repo", config.get("adapter_repo") == EXPECTED_ADAPTER_REPO, str(config.get("adapter_repo")))
    add_check(checks, "config_no_limit", config.get("limit") is None, str(config.get("limit")))
    add_check(checks, "config_selected_tasks", config.get("tasks") == EXPECTED_TASKS, str(config.get("tasks")))
    add_check(checks, "config_timeout_bounded", int(config.get("timeout_s", 0)) == 21600, str(config.get("timeout_s")))
    add_check(checks, "dry_run_status", dry_run.get("status") == "dry-run", str(dry_run.get("status")))
    add_check(checks, "dry_run_no_execute", dry_run.get("execute") is False, str(dry_run.get("execute")))
    add_check(checks, "dry_run_no_confirmation", dry_run.get("confirm_kaggle_run") is False, str(dry_run.get("confirm_kaggle_run")))
    add_check(checks, "dry_run_no_blockers", dry_run.get("blockers") == [], str(dry_run.get("blockers")))
    add_check(checks, "preflight_kaggle_prepared", kaggle_status == "prepared-needs-notebook-contract", str(kaggle_status))
    add_check(checks, "preflight_quota_visible", quota_probe.get("returncode") == 0, str(quota_probe.get("returncode")))
    add_check(
        checks,
        "runner_downloads_public_adapter",
        "snapshot_download(repo_id=adapter_repo" in runner_text and "PEFT_ADAPTER_REPO" in runner_text,
        "adapter repo is configurable and defaults to the public PEFT repo",
    )
    add_check(
        checks,
        "runner_writes_kaggle_working_artifacts",
        "/kaggle/working" in runner_text and "result_json" in runner_text and "output_dir" in runner_text,
        "runner writes summary and lm-eval outputs under Kaggle working directory",
    )
    add_check(
        checks,
        "runner_records_claim_boundary",
        "No-limit benchmark claim only if every configured task completes without --limit." in runner_text,
        "claim boundary is embedded in runner output",
    )

    passed = all(check["passed"] for check in checks)
    return {
        "status": "pass" if passed else "fail",
        "staging_dir": str(staging_dir),
        "dry_run": str(dry_run_path),
        "preflight": str(preflight_path),
        "dataset_terms_contract": {
            "private_data_upload": False,
            "public_inputs": [
                EXPECTED_ADAPTER_REPO,
                "Qwen/Qwen3-4B",
                "lm-eval selected public benchmark tasks",
            ],
            "internet_required": True,
            "operator_boundary": "No Kaggle kernel push without --execute --confirm-kaggle-run and explicit operator approval.",
        },
        "checks": checks,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 V4 PEFT Kaggle Notebook Contract",
        "",
        f"Status: `{report['status']}`",
        f"Staging dir: `{report['staging_dir']}`",
        f"Dry-run report: `{report['dry_run']}`",
        f"Preflight report: `{report['preflight']}`",
        "",
        "## Dataset And Execution Contract",
        "",
        "- Private data upload: `False`",
        "- Public inputs: `edithatogo/qwen3-4b-hermes-lora-peft-converted`, `Qwen/Qwen3-4B`, lm-eval selected public benchmark tasks",
        "- Internet is required for public dependency/model downloads inside Kaggle.",
        "- No Kaggle kernel push without `--execute --confirm-kaggle-run` and explicit operator approval.",
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
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING_DIR)
    parser.add_argument("--dry-run", type=Path, default=DEFAULT_DRY_RUN)
    parser.add_argument("--preflight", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    report = validate_contract(args.staging_dir, args.dry_run, args.preflight)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
