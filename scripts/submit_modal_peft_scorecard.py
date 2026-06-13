#!/usr/bin/env python3
"""Build or submit a guarded Modal PEFT scorecard command."""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ID = "qwen3-v4-peft-modal-lm-eval-selected-full-20260614"
DEFAULT_STAGING_DIR = ROOT / "reports/cloud/modal-qwen3-v4-peft-scorecard-20260614"
DEFAULT_APP = ROOT / "scripts/modal_peft_lm_eval_selected.py"
DEFAULT_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"
DEFAULT_ADAPTER_REPO = "edithatogo/qwen3-4b-hermes-lora-peft-converted"
BACKEND_PREFLIGHT_REPORT = ROOT / "reports/cloud/backend-preflight-20260613.json"


@dataclass(frozen=True)
class ModalScorecardSpec:
    run_id: str
    staging_dir: Path
    app_path: Path
    timeout_s: int
    gpu: str
    tasks: str
    adapter_repo: str


def known_modal_policy_gate(report_path: Path = BACKEND_PREFLIGHT_REPORT) -> bool:
    if not report_path.exists():
        return True
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return True
    modal = report.get("backends", {}).get("modal", {})
    return modal.get("status") != "prepared-needs-credit-and-gpu-policy-check"


def modal_config(spec: ModalScorecardSpec) -> dict[str, Any]:
    return {
        "run_id": spec.run_id,
        "adapter_repo": spec.adapter_repo,
        "base_model": "Qwen/Qwen3-4B",
        "tasks": spec.tasks,
        "limit": None,
        "timeout_s": spec.timeout_s,
        "output_dir": f"/results/{spec.run_id}/lm-eval-output",
        "result_json": f"/results/{spec.run_id}/summary.json",
    }


def stage_config(spec: ModalScorecardSpec) -> dict[str, str]:
    spec.staging_dir.mkdir(parents=True, exist_ok=True)
    config_path = spec.staging_dir / "modal-peft-lm-eval-config.json"
    config_path.write_text(json.dumps(modal_config(spec), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"config": str(config_path), "app": str(spec.app_path)}


def build_modal_command(spec: ModalScorecardSpec) -> list[str]:
    config_json = json.dumps(modal_config(spec), sort_keys=True)
    return [
        "modal",
        "run",
        "--name",
        spec.run_id,
        "--write-result",
        str(spec.staging_dir / "modal-result.json"),
        f"{spec.app_path}::scorecard",
        "--config-json",
        config_json,
    ]


def render_shell(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def build_report(
    spec: ModalScorecardSpec,
    staged: dict[str, str],
    command: list[str],
    execute: bool,
    confirm_modal_run: bool,
    confirm_zero_cost_compute: bool,
    modal_policy_gate_observed: bool = False,
    ignore_modal_policy_gate: bool = False,
) -> dict[str, Any]:
    status = "ready-to-submit" if execute and confirm_modal_run and confirm_zero_cost_compute else "dry-run"
    blockers: list[str] = []
    if execute and not confirm_modal_run:
        status = "blocked"
        blockers.append("--confirm-modal-run is required with --execute")
    if execute and not confirm_zero_cost_compute:
        status = "blocked"
        blockers.append("--confirm-zero-cost-compute is required with --execute")
    if execute and modal_policy_gate_observed and not ignore_modal_policy_gate:
        status = "blocked"
        blockers.append("Modal backend preflight is not in the prepared credit/GPU-policy state; rerun preflight or pass --ignore-modal-policy-gate after verification")
    return {
        "status": status,
        "run_id": spec.run_id,
        "backend": "modal",
        "execute": execute,
        "confirm_modal_run": confirm_modal_run,
        "confirm_zero_cost_compute": confirm_zero_cost_compute,
        "modal_policy_gate_observed": modal_policy_gate_observed,
        "ignore_modal_policy_gate": ignore_modal_policy_gate,
        "gpu": spec.gpu,
        "timeout_s": spec.timeout_s,
        "adapter_repo": spec.adapter_repo,
        "tasks": spec.tasks,
        "staging_dir": str(spec.staging_dir),
        "staged": staged,
        "command": command,
        "shell_command": render_shell(command),
        "blockers": blockers,
        "claim_boundary": "No-limit benchmark claim only after Modal completes every configured task without --limit and artifacts are recovered from the Modal volume/result file.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING_DIR)
    parser.add_argument("--app-path", type=Path, default=DEFAULT_APP)
    parser.add_argument("--timeout-s", type=int, default=21600)
    parser.add_argument("--gpu", default="T4")
    parser.add_argument("--tasks", default=DEFAULT_TASKS)
    parser.add_argument("--adapter-repo", default=DEFAULT_ADAPTER_REPO)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-modal-run", action="store_true")
    parser.add_argument("--confirm-zero-cost-compute", action="store_true")
    parser.add_argument("--ignore-modal-policy-gate", action="store_true")
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    spec = ModalScorecardSpec(
        run_id=args.run_id,
        staging_dir=args.staging_dir,
        app_path=args.app_path,
        timeout_s=args.timeout_s,
        gpu=args.gpu,
        tasks=args.tasks,
        adapter_repo=args.adapter_repo,
    )
    staged = stage_config(spec)
    command = build_modal_command(spec)
    report = build_report(
        spec,
        staged,
        command,
        args.execute,
        args.confirm_modal_run,
        args.confirm_zero_cost_compute,
        modal_policy_gate_observed=known_modal_policy_gate(),
        ignore_modal_policy_gate=args.ignore_modal_policy_gate,
    )

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.execute and report["blockers"]:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 2

    if args.execute:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        report["submission"] = {
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
        print(json.dumps(report, indent=2, sort_keys=True))
        return result.returncode

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
