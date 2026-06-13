#!/usr/bin/env python3
"""Build or submit a guarded NGC Cloud Function task for the PEFT scorecard."""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND_PREFLIGHT_REPORT = ROOT / "reports/cloud/backend-preflight-20260613.json"
DEFAULT_RUN_ID = "qwen3-v4-peft-ngc-lm-eval-selected-full-20260613"
DEFAULT_TASK_NAME = "qwen3-v4-peft-lm-eval-selected-full"
DEFAULT_ADAPTER_REPO = "edithatogo/qwen3-4b-hermes-lora-peft-converted"
DEFAULT_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"
DEFAULT_CONTAINER_IMAGE = "REPLACE_WITH_NGC_REGISTRY_IMAGE"
DEFAULT_GPU_SPEC = "REPLACE_WITH_GPU_SPEC"


@dataclass(frozen=True)
class NgcCloudFunctionScorecardSpec:
    run_id: str
    task_name: str
    adapter_repo: str
    tasks: str
    container_image: str
    gpu_specification: str
    max_runtime_duration: str


def known_ngc_auth_blocker(report_path: Path = BACKEND_PREFLIGHT_REPORT) -> bool:
    if not report_path.exists():
        return False
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    ngc = report.get("backends", {}).get("ngc", {})
    return ngc.get("status") == "blocked"


def build_task_command(spec: NgcCloudFunctionScorecardSpec) -> list[str]:
    return [
        "ngc",
        "cloud-function",
        "task",
        "create",
        "--name",
        spec.task_name,
        "--gpu-specification",
        spec.gpu_specification,
        "--container-image",
        spec.container_image,
        "--container-environment-variable",
        f"RUN_ID:{spec.run_id}",
        "--container-environment-variable",
        f"PEFT_ADAPTER_REPO:{spec.adapter_repo}",
        "--container-environment-variable",
        f"LM_EVAL_TASKS:{spec.tasks}",
        "--container-environment-variable",
        "LM_EVAL_TIMEOUT_S:21600",
        "--max-runtime-duration",
        spec.max_runtime_duration,
        "--result-handling-strategy",
        "UPLOAD",
    ]


def render_shell(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def build_report(
    spec: NgcCloudFunctionScorecardSpec,
    command: list[str],
    execute: bool,
    confirm_ngc_run: bool,
    auth_blocker_observed: bool = False,
    ignore_known_auth_blocker: bool = False,
) -> dict[str, Any]:
    blockers: list[str] = []
    if execute and not confirm_ngc_run:
        blockers.append("--confirm-ngc-run is required with --execute")
    if execute and auth_blocker_observed and not ignore_known_auth_blocker:
        blockers.append("known NGC auth/entitlement blocker is still recorded; configure NGC or pass --ignore-known-auth-blocker after verification")
    if execute and spec.container_image == DEFAULT_CONTAINER_IMAGE:
        blockers.append("--container-image must be set to a real NGC registry image before execution")
    if execute and spec.gpu_specification == DEFAULT_GPU_SPEC:
        blockers.append("--gpu-specification must be set from NGC quota/capacity before execution")

    status = "dry-run"
    if execute and blockers:
        status = "blocked"
    elif execute:
        status = "ready-to-submit"

    return {
        "status": status,
        "run_id": spec.run_id,
        "backend": "ngc-cloud-function",
        "execute": execute,
        "confirm_ngc_run": confirm_ngc_run,
        "auth_blocker_observed": auth_blocker_observed,
        "ignore_known_auth_blocker": ignore_known_auth_blocker,
        "task_name": spec.task_name,
        "adapter_repo": spec.adapter_repo,
        "tasks": spec.tasks,
        "container_image": spec.container_image,
        "gpu_specification": spec.gpu_specification,
        "max_runtime_duration": spec.max_runtime_duration,
        "command": command,
        "shell_command": render_shell(command),
        "blockers": blockers,
        "claim_boundary": "No benchmark claim until NGC completes every configured task and artifacts are recovered.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--task-name", default=DEFAULT_TASK_NAME)
    parser.add_argument("--adapter-repo", default=DEFAULT_ADAPTER_REPO)
    parser.add_argument("--tasks", default=DEFAULT_TASKS)
    parser.add_argument("--container-image", default=DEFAULT_CONTAINER_IMAGE)
    parser.add_argument("--gpu-specification", default=DEFAULT_GPU_SPEC)
    parser.add_argument("--max-runtime-duration", default="6H")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-ngc-run", action="store_true")
    parser.add_argument("--ignore-known-auth-blocker", action="store_true")
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    spec = NgcCloudFunctionScorecardSpec(
        run_id=args.run_id,
        task_name=args.task_name,
        adapter_repo=args.adapter_repo,
        tasks=args.tasks,
        container_image=args.container_image,
        gpu_specification=args.gpu_specification,
        max_runtime_duration=args.max_runtime_duration,
    )
    command = build_task_command(spec)
    report = build_report(
        spec,
        command,
        args.execute,
        args.confirm_ngc_run,
        auth_blocker_observed=known_ngc_auth_blocker(),
        ignore_known_auth_blocker=args.ignore_known_auth_blocker,
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
