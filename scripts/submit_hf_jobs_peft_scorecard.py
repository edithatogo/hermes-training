#!/usr/bin/env python3
"""Build or submit the guarded Hugging Face Jobs PEFT scorecard command."""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_RUN_ID = "qwen3-v4-peft-hf-jobs-lm-eval-selected-full-20260613"
DEFAULT_RESULTS_REPO = "edithatogo/qwen3-v4-peft-lm-eval-results"
DEFAULT_ADAPTER_REPO = "edithatogo/qwen3-4b-hermes-lora-peft-converted"
DEFAULT_IMAGE = "pytorch/pytorch:2.7.1-cuda12.6-cudnn9-runtime"
DEFAULT_SCRIPT_URL = (
    "https://raw.githubusercontent.com/edithatogo/hermes-training/main/scripts/hf_jobs_peft_lm_eval_selected.py"
)
DEFAULT_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"
HF_JOBS_SCORECARD_REPORT = Path("reports/cloud/qwen3-v4-peft-hf-jobs-scorecard-plan-20260613.md")


@dataclass(frozen=True)
class HfJobsScorecardSpec:
    run_id: str
    results_repo: str
    adapter_repo: str
    flavor: str
    timeout: str
    image: str
    tasks: str
    script_url: str
    detach: bool = True


def build_job_command(spec: HfJobsScorecardSpec) -> list[str]:
    payload = (
        'python -m pip install --quiet --upgrade "lm_eval[hf]" '
        '"transformers>=4.56,<5" peft bitsandbytes safetensors accelerate huggingface_hub && '
        f"curl -L {shlex.quote(spec.script_url)} -o /tmp/hf_jobs_peft_lm_eval_selected.py && "
        "python /tmp/hf_jobs_peft_lm_eval_selected.py"
    )
    command = [
        "hf",
        "jobs",
        "run",
        "--flavor",
        spec.flavor,
        "--timeout",
        spec.timeout,
    ]
    if spec.detach:
        command.append("--detach")
    command.extend(
        [
            "--secrets",
            "HF_TOKEN",
            "-e",
            f"RUN_ID={spec.run_id}",
            "-e",
            f"HF_RESULTS_REPO={spec.results_repo}",
            "-e",
            f"LM_EVAL_TASKS={spec.tasks}",
            "-e",
            "LM_EVAL_TIMEOUT_S=21600",
            "-v",
            f"hf://models/{spec.adapter_repo}:/adapter:ro",
            spec.image,
            "bash",
            "-lc",
            payload,
        ]
    )
    return command


def render_shell(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def known_credit_blocker(report_path: Path = HF_JOBS_SCORECARD_REPORT) -> bool:
    if not report_path.exists():
        return False
    report = report_path.read_text(encoding="utf-8")
    return "402 Payment Required" in report or "Pre-paid credit balance is insufficient" in report


def build_report(
    spec: HfJobsScorecardSpec,
    command: list[str],
    execute: bool,
    confirm_paid_compute: bool,
    credit_blocker_observed: bool = False,
    ignore_known_credit_blocker: bool = False,
) -> dict[str, Any]:
    status = "ready-to-submit" if execute and confirm_paid_compute else "dry-run"
    blockers: list[str] = []
    if execute and not confirm_paid_compute:
        status = "blocked"
        blockers.append("--confirm-paid-compute is required with --execute")
    if execute and credit_blocker_observed and not ignore_known_credit_blocker:
        status = "blocked"
        blockers.append("known HF Jobs prepaid credit blocker is still recorded; add credits or pass --ignore-known-credit-blocker after verifying credits")
    return {
        "status": status,
        "run_id": spec.run_id,
        "backend": "hf-jobs",
        "paid_compute": True,
        "confirm_paid_compute": confirm_paid_compute,
        "credit_blocker_observed": credit_blocker_observed,
        "ignore_known_credit_blocker": ignore_known_credit_blocker,
        "execute": execute,
        "flavor": spec.flavor,
        "timeout": spec.timeout,
        "adapter_repo": spec.adapter_repo,
        "results_repo": spec.results_repo,
        "tasks": spec.tasks,
        "command": command,
        "shell_command": render_shell(command),
        "blockers": blockers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--results-repo", default=DEFAULT_RESULTS_REPO)
    parser.add_argument("--adapter-repo", default=DEFAULT_ADAPTER_REPO)
    parser.add_argument("--flavor", default="t4-small")
    parser.add_argument("--timeout", default="8h")
    parser.add_argument("--image", default=DEFAULT_IMAGE)
    parser.add_argument("--tasks", default=DEFAULT_TASKS)
    parser.add_argument("--script-url", default=DEFAULT_SCRIPT_URL)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-paid-compute", action="store_true")
    parser.add_argument("--ignore-known-credit-blocker", action="store_true")
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    spec = HfJobsScorecardSpec(
        run_id=args.run_id,
        results_repo=args.results_repo,
        adapter_repo=args.adapter_repo,
        flavor=args.flavor,
        timeout=args.timeout,
        image=args.image,
        tasks=args.tasks,
        script_url=args.script_url,
    )
    command = build_job_command(spec)
    report = build_report(
        spec,
        command,
        args.execute,
        args.confirm_paid_compute,
        credit_blocker_observed=known_credit_blocker(),
        ignore_known_credit_blocker=args.ignore_known_credit_blocker,
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
