#!/usr/bin/env python3
"""Validate the staged Modal PEFT scorecard execution contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STAGING_DIR = ROOT / "reports/cloud/modal-qwen3-v4-peft-scorecard-20260614"
DEFAULT_DRY_RUN = ROOT / "reports/cloud/qwen3-v4-peft-modal-submit-dry-run-20260614.json"
DEFAULT_APP = ROOT / "scripts/modal_peft_lm_eval_selected.py"
DEFAULT_JSON = ROOT / "reports/cloud/qwen3-v4-peft-modal-contract-20260614.json"
DEFAULT_MARKDOWN = ROOT / "reports/cloud/qwen3-v4-peft-modal-contract-20260614.md"
EXPECTED_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"
EXPECTED_ADAPTER_REPO = "edithatogo/qwen3-4b-hermes-lora-peft-converted"
EXPECTED_BASE_MODEL = "Qwen/Qwen3-4B"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": passed, "detail": detail})


def validate_contract(staging_dir: Path, dry_run_path: Path, app_path: Path) -> dict[str, Any]:
    config_path = staging_dir / "modal-peft-lm-eval-config.json"
    config = load_json(config_path)
    dry_run = load_json(dry_run_path)
    app_text = app_path.read_text(encoding="utf-8")
    command = dry_run.get("command", [])
    command_text = " ".join(str(item) for item in command) if isinstance(command, list) else str(command)
    checks: list[dict[str, Any]] = []

    add_check(checks, "dry_run_status", dry_run.get("status") == "dry-run", str(dry_run.get("status")))
    add_check(checks, "dry_run_no_execute", dry_run.get("execute") is False, str(dry_run.get("execute")))
    add_check(checks, "dry_run_no_confirmation", dry_run.get("confirm_modal_run") is False, str(dry_run.get("confirm_modal_run")))
    add_check(
        checks,
        "dry_run_no_zero_cost_confirmation",
        dry_run.get("confirm_zero_cost_compute") is False,
        str(dry_run.get("confirm_zero_cost_compute")),
    )
    add_check(checks, "dry_run_no_blockers", dry_run.get("blockers") == [], str(dry_run.get("blockers")))
    add_check(checks, "command_uses_modal_run", isinstance(command, list) and command[:2] == ["modal", "run"], command_text[:240])
    add_check(checks, "command_targets_scorecard", "::scorecard" in command_text, command_text[:240])
    add_check(checks, "command_writes_local_result", "--write-result" in command_text and "modal-result.json" in command_text, command_text[:240])

    add_check(checks, "config_adapter_public_repo", config.get("adapter_repo") == EXPECTED_ADAPTER_REPO, str(config.get("adapter_repo")))
    add_check(checks, "config_base_model", config.get("base_model") == EXPECTED_BASE_MODEL, str(config.get("base_model")))
    add_check(checks, "config_no_limit", config.get("limit") is None, str(config.get("limit")))
    add_check(checks, "config_selected_tasks", config.get("tasks") == EXPECTED_TASKS, str(config.get("tasks")))
    add_check(checks, "config_timeout_bounded", int(config.get("timeout_s", 0)) == 21600, str(config.get("timeout_s")))
    add_check(checks, "config_volume_output", str(config.get("output_dir", "")).startswith("/results/"), str(config.get("output_dir")))
    add_check(checks, "config_volume_summary", str(config.get("result_json", "")).startswith("/results/"), str(config.get("result_json")))

    add_check(checks, "app_declares_t4_gpu", '@app.function(image=image, gpu="T4"' in app_text, "Modal function uses T4 GPU")
    add_check(checks, "app_uses_results_volume", "modal.Volume.from_name" in app_text and 'volumes={"/results": results_volume}' in app_text, "Modal volume mounted at /results")
    add_check(checks, "app_commits_volume", "results_volume.commit()" in app_text, "Modal result volume commit is attempted")
    add_check(checks, "app_embeds_claim_boundary", "No-limit benchmark claim only if every configured task completes without --limit." in app_text, "claim boundary is embedded")

    passed = all(check["passed"] for check in checks)
    return {
        "status": "pass" if passed else "fail",
        "staging_dir": str(staging_dir),
        "dry_run": str(dry_run_path),
        "app": str(app_path),
        "execution_contract": {
            "execute": False,
            "remote_run_requires": [
                "--execute",
                "--confirm-modal-run",
                "--confirm-zero-cost-compute",
                "cost or zero-cost policy evidence",
                "post-run result ingest validation",
            ],
            "claim_boundary": "No benchmark claim until Modal returns scored no-limit results for all selected tasks.",
        },
        "checks": checks,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 V4 PEFT Modal Scorecard Contract",
        "",
        f"Status: `{report['status']}`",
        f"Staging dir: `{report['staging_dir']}`",
        f"Dry-run report: `{report['dry_run']}`",
        f"App: `{report['app']}`",
        "",
        "## Execution Contract",
        "",
        "- Dry-run only: `execute=false`",
        "- Remote execution requires `--execute --confirm-modal-run --confirm-zero-cost-compute`.",
        "- Cost or zero-cost policy evidence is required before execution.",
        "- Post-run result ingest validation is required before benchmark claims.",
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
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    report = validate_contract(args.staging_dir, args.dry_run, args.app)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
