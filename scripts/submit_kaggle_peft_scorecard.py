#!/usr/bin/env python3
"""Build or submit a guarded Kaggle kernel for the Qwen3 v4 PEFT scorecard."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ID = "qwen3-v4-peft-kaggle-lm-eval-selected-full-20260613"
DEFAULT_KERNEL_ID = "edithatogo/qwen3-v4-peft-lm-eval-selected-full"
DEFAULT_STAGING_DIR = ROOT / "reports/cloud/kaggle-qwen3-v4-peft-scorecard-20260613"
DEFAULT_RUNNER = ROOT / "scripts/kaggle_peft_lm_eval_selected.py"
DEFAULT_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"
BACKEND_PREFLIGHT_REPORT = ROOT / "reports/cloud/backend-preflight-20260613.json"


@dataclass(frozen=True)
class KaggleScorecardSpec:
    run_id: str
    kernel_id: str
    staging_dir: Path
    runner_path: Path
    timeout_s: int
    accelerator: str
    tasks: str
    adapter_repo: str
    public_kernel: bool = True


def kernel_metadata(spec: KaggleScorecardSpec) -> dict[str, Any]:
    return {
        "id": spec.kernel_id,
        "title": "Qwen3 v4 PEFT lm-eval selected full",
        "code_file": "kaggle_peft_lm_eval_selected.py",
        "language": "python",
        "kernel_type": "script",
        "is_private": not spec.public_kernel,
        "enable_gpu": True,
        "enable_internet": True,
        "keywords": ["qwen3", "hermes", "peft", "lm-eval"],
        "license": "apache-2.0",
    }


def build_push_command(spec: KaggleScorecardSpec) -> list[str]:
    return [
        "kaggle",
        "kernels",
        "push",
        "--path",
        str(spec.staging_dir),
        "--timeout",
        str(spec.timeout_s),
        "--accelerator",
        spec.accelerator,
    ]


def known_kaggle_auth_blocker(report_path: Path = BACKEND_PREFLIGHT_REPORT) -> bool:
    if not report_path.exists():
        return False
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    kaggle = report.get("backends", {}).get("kaggle", {})
    return kaggle.get("status") == "blocked-needs-auth"


def stage_kernel(spec: KaggleScorecardSpec) -> dict[str, str]:
    spec.staging_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = spec.staging_dir / "kernel-metadata.json"
    config_path = spec.staging_dir / "kaggle-peft-lm-eval-config.json"
    runner_target = spec.staging_dir / "kaggle_peft_lm_eval_selected.py"
    metadata_path.write_text(json.dumps(kernel_metadata(spec), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    config_path.write_text(
        json.dumps(
            {
                "run_id": spec.run_id,
                "adapter_repo": spec.adapter_repo,
                "tasks": spec.tasks,
                "limit": None,
                "timeout_s": spec.timeout_s,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    shutil.copy2(spec.runner_path, runner_target)
    return {"metadata": str(metadata_path), "config": str(config_path), "runner": str(runner_target)}


def build_report(
    spec: KaggleScorecardSpec,
    staged: dict[str, str],
    command: list[str],
    execute: bool,
    confirm_kaggle_run: bool,
    auth_blocker_observed: bool = False,
    ignore_known_auth_blocker: bool = False,
) -> dict[str, Any]:
    status = "ready-to-submit" if execute and confirm_kaggle_run else "dry-run"
    blockers: list[str] = []
    if execute and not confirm_kaggle_run:
        status = "blocked"
        blockers.append("--confirm-kaggle-run is required with --execute")
    if execute and auth_blocker_observed and not ignore_known_auth_blocker:
        status = "blocked"
        blockers.append("known Kaggle authentication blocker is still recorded; authenticate or pass --ignore-known-auth-blocker after verifying auth")
    return {
        "status": status,
        "run_id": spec.run_id,
        "backend": "kaggle-kernels",
        "execute": execute,
        "confirm_kaggle_run": confirm_kaggle_run,
        "auth_blocker_observed": auth_blocker_observed,
        "ignore_known_auth_blocker": ignore_known_auth_blocker,
        "kernel_id": spec.kernel_id,
        "staging_dir": str(spec.staging_dir),
        "staged": staged,
        "timeout_s": spec.timeout_s,
        "accelerator": spec.accelerator,
        "adapter_repo": spec.adapter_repo,
        "tasks": spec.tasks,
        "command": command,
        "blockers": blockers,
        "claim_boundary": "No-limit benchmark claim only after Kaggle completes every configured task without --limit.",
    }


def write_json_report(path: Path | None, report: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--kernel-id", default=DEFAULT_KERNEL_ID)
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING_DIR)
    parser.add_argument("--runner-path", type=Path, default=DEFAULT_RUNNER)
    parser.add_argument("--timeout-s", type=int, default=21600)
    parser.add_argument("--accelerator", default="gpu")
    parser.add_argument("--tasks", default=DEFAULT_TASKS)
    parser.add_argument("--adapter-repo", default="edithatogo/qwen3-4b-hermes-lora-peft-converted")
    parser.add_argument("--private-kernel", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-kaggle-run", action="store_true")
    parser.add_argument("--ignore-known-auth-blocker", action="store_true")
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    spec = KaggleScorecardSpec(
        run_id=args.run_id,
        kernel_id=args.kernel_id,
        staging_dir=args.staging_dir,
        runner_path=args.runner_path,
        timeout_s=args.timeout_s,
        accelerator=args.accelerator,
        tasks=args.tasks,
        adapter_repo=args.adapter_repo,
        public_kernel=not args.private_kernel,
    )
    staged = stage_kernel(spec)
    command = build_push_command(spec)
    report = build_report(
        spec,
        staged,
        command,
        args.execute,
        args.confirm_kaggle_run,
        auth_blocker_observed=known_kaggle_auth_blocker(),
        ignore_known_auth_blocker=args.ignore_known_auth_blocker,
    )

    write_json_report(args.json_output, report)

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
        write_json_report(args.json_output, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return result.returncode

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
