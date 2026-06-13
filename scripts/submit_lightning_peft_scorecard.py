#!/usr/bin/env python3
"""Build or submit a guarded Lightning Jobs PEFT scorecard command."""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ID = "qwen3-v4-peft-lightning-lm-eval-selected-full-20260614"
DEFAULT_ADAPTER_REPO = "edithatogo/qwen3-4b-hermes-lora-peft-converted"
DEFAULT_IMAGE = "pytorch/pytorch:2.7.1-cuda12.6-cudnn9-runtime"
DEFAULT_SCRIPT_URL = (
    "https://raw.githubusercontent.com/edithatogo/hermes-training/main/scripts/hf_jobs_peft_lm_eval_selected.py"
)
DEFAULT_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"
DEFAULT_STAGING_DIR = ROOT / "reports/cloud/lightning-qwen3-v4-peft-scorecard-20260614"
BACKEND_PREFLIGHT_REPORT = ROOT / "reports/cloud/backend-preflight-20260613.json"
TEAMSPACE_PLACEHOLDER = "<owner>/<teamspace>"


@dataclass(frozen=True)
class LightningScorecardSpec:
    run_id: str
    staging_dir: Path
    teamspace: str
    machine: str
    image: str
    script_url: str
    tasks: str
    adapter_repo: str
    timeout_s: int


def known_lightning_teamspace_blocker(report_path: Path = BACKEND_PREFLIGHT_REPORT) -> bool:
    if not report_path.exists():
        return True
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return True
    lightning = report.get("backends", {}).get("lightning", {})
    return lightning.get("status") in {"blocked-needs-teamspace-owner", "blocked-needs-auth-or-teamspace", "blocked"}


def job_payload(spec: LightningScorecardSpec) -> str:
    return (
        "python -m pip install --quiet --upgrade \"lm_eval[hf]\" "
        "\"transformers>=4.56,<5\" peft bitsandbytes safetensors accelerate huggingface_hub && "
        f"curl -L {shlex.quote(spec.script_url)} -o /tmp/hf_jobs_peft_lm_eval_selected.py && "
        f"RUN_ID={shlex.quote(spec.run_id)} "
        f"PEFT_ADAPTER_REPO={shlex.quote(spec.adapter_repo)} "
        f"LM_EVAL_TASKS={shlex.quote(spec.tasks)} "
        f"LM_EVAL_TIMEOUT_S={spec.timeout_s} "
        f"LM_EVAL_RESULT_JSON=/tmp/{shlex.quote(spec.run_id)}-summary.json "
        f"LM_EVAL_OUTPUT_DIR=/tmp/{shlex.quote(spec.run_id)}-lm-eval-output "
        "python /tmp/hf_jobs_peft_lm_eval_selected.py"
    )


def build_lightning_command(spec: LightningScorecardSpec) -> list[str]:
    command = [
        "lightning",
        "job",
        "run",
        "--name",
        spec.run_id,
        "--machine",
        spec.machine,
        "--teamspace",
        spec.teamspace,
        "--image",
        spec.image,
        "--command",
        job_payload(spec),
    ]
    return command


def render_shell(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def stage_config(spec: LightningScorecardSpec) -> dict[str, str]:
    spec.staging_dir.mkdir(parents=True, exist_ok=True)
    config_path = spec.staging_dir / "lightning-peft-lm-eval-config.json"
    config_path.write_text(
        json.dumps(
            {
                "run_id": spec.run_id,
                "teamspace": spec.teamspace,
                "machine": spec.machine,
                "image": spec.image,
                "adapter_repo": spec.adapter_repo,
                "tasks": spec.tasks,
                "limit": None,
                "timeout_s": spec.timeout_s,
                "artifact_persistence": "unproven until a real Lightning job writes and recovered outputs are copied to the SSD",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {"config": str(config_path)}


def build_report(
    spec: LightningScorecardSpec,
    staged: dict[str, str],
    command: list[str],
    execute: bool,
    confirm_lightning_run: bool,
    confirm_zero_cost_compute: bool,
    teamspace_blocker_observed: bool = False,
    ignore_teamspace_blocker: bool = False,
) -> dict[str, Any]:
    status = "ready-to-submit" if execute and confirm_lightning_run and confirm_zero_cost_compute else "dry-run"
    blockers: list[str] = []
    if execute and not confirm_lightning_run:
        status = "blocked"
        blockers.append("--confirm-lightning-run is required with --execute")
    if execute and not confirm_zero_cost_compute:
        status = "blocked"
        blockers.append("--confirm-zero-cost-compute is required with --execute")
    if execute and spec.teamspace == TEAMSPACE_PLACEHOLDER:
        status = "blocked"
        blockers.append("--teamspace must be a real owner/teamspace value with --execute")
    if execute and teamspace_blocker_observed and not ignore_teamspace_blocker:
        status = "blocked"
        blockers.append("known Lightning teamspace blocker is still recorded; configure teamspace or pass --ignore-teamspace-blocker after verification")
    return {
        "status": status,
        "run_id": spec.run_id,
        "backend": "lightning-jobs",
        "execute": execute,
        "confirm_lightning_run": confirm_lightning_run,
        "confirm_zero_cost_compute": confirm_zero_cost_compute,
        "teamspace_blocker_observed": teamspace_blocker_observed,
        "ignore_teamspace_blocker": ignore_teamspace_blocker,
        "teamspace": spec.teamspace,
        "machine": spec.machine,
        "image": spec.image,
        "adapter_repo": spec.adapter_repo,
        "tasks": spec.tasks,
        "timeout_s": spec.timeout_s,
        "staging_dir": str(spec.staging_dir),
        "staged": staged,
        "command": command,
        "shell_command": render_shell(command),
        "blockers": blockers,
        "claim_boundary": "No benchmark claim until a Lightning job completes all configured tasks without --limit and artifacts are recovered to the SSD.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING_DIR)
    parser.add_argument("--teamspace", default=TEAMSPACE_PLACEHOLDER)
    parser.add_argument("--machine", default="T4")
    parser.add_argument("--image", default=DEFAULT_IMAGE)
    parser.add_argument("--script-url", default=DEFAULT_SCRIPT_URL)
    parser.add_argument("--tasks", default=DEFAULT_TASKS)
    parser.add_argument("--adapter-repo", default=DEFAULT_ADAPTER_REPO)
    parser.add_argument("--timeout-s", type=int, default=21600)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-lightning-run", action="store_true")
    parser.add_argument("--confirm-zero-cost-compute", action="store_true")
    parser.add_argument("--ignore-teamspace-blocker", action="store_true")
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    spec = LightningScorecardSpec(
        run_id=args.run_id,
        staging_dir=args.staging_dir,
        teamspace=args.teamspace,
        machine=args.machine,
        image=args.image,
        script_url=args.script_url,
        tasks=args.tasks,
        adapter_repo=args.adapter_repo,
        timeout_s=args.timeout_s,
    )
    staged = stage_config(spec)
    command = build_lightning_command(spec)
    report = build_report(
        spec,
        staged,
        command,
        args.execute,
        args.confirm_lightning_run,
        args.confirm_zero_cost_compute,
        teamspace_blocker_observed=known_lightning_teamspace_blocker(),
        ignore_teamspace_blocker=args.ignore_teamspace_blocker,
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
