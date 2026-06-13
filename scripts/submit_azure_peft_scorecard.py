#!/usr/bin/env python3
"""Build or submit a guarded Azure ML job for the Qwen3 v4 PEFT scorecard."""
from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JOB_TEMPLATE = ROOT / "templates/azure/qwen3-v4-peft-lm-eval-job.yaml"
DEFAULT_RUN_ID = "qwen3-v4-peft-azure-lm-eval-selected-full-20260613"
DEFAULT_RESOURCE_GROUP = "hermes-ml-rg"
DEFAULT_WORKSPACE = "hermes-ml-lab"
DEFAULT_REGION = "australiaeast"
DEFAULT_COMPUTE = "azureml:hermes-lowpri-t4"


@dataclass(frozen=True)
class AzureScorecardSpec:
    run_id: str
    resource_group: str
    workspace: str
    region: str
    compute: str
    job_template: Path


def run_command(command: list[str], timeout_s: int = 30) -> dict[str, Any]:
    executable = shutil.which(command[0])
    if not executable:
        return {
            "installed": False,
            "command": command,
            "returncode": None,
            "stdout": "",
            "stderr": f"{command[0]} not found on PATH",
        }
    result = subprocess.run(
        [executable, *command[1:]],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )
    return {
        "installed": True,
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def azure_preflight(spec: AzureScorecardSpec) -> dict[str, Any]:
    account = run_command(["az", "account", "show", "-o", "json"])
    extension = run_command(["az", "extension", "show", "-n", "ml", "--query", "version", "-o", "tsv"])
    template_exists = spec.job_template.exists()
    ready = (
        account["installed"]
        and account["returncode"] == 0
        and extension["returncode"] == 0
        and template_exists
    )
    blockers: list[str] = []
    if not account["installed"]:
        blockers.append("Azure CLI is not installed")
    elif account["returncode"] != 0:
        blockers.append(account["stderr"] or account["stdout"] or "az account show failed")
    if extension["returncode"] != 0:
        blockers.append("Azure ML CLI extension is missing or unavailable")
    if not template_exists:
        blockers.append(f"missing job template: {spec.job_template}")
    return {
        "ready": ready,
        "account": account,
        "ml_extension": extension,
        "template_exists": template_exists,
        "blockers": blockers,
    }


def build_submit_command(spec: AzureScorecardSpec) -> list[str]:
    return [
        "az",
        "ml",
        "job",
        "create",
        "--file",
        str(spec.job_template),
        "--resource-group",
        spec.resource_group,
        "--workspace-name",
        spec.workspace,
        "--set",
        f"name={spec.run_id}",
        f"compute={spec.compute}",
    ]


def build_report(spec: AzureScorecardSpec, execute: bool, confirm_azure_run: bool) -> dict[str, Any]:
    command = build_submit_command(spec)
    preflight = azure_preflight(spec)
    blockers = list(preflight["blockers"])
    status = "blocked" if blockers else "dry-run"
    if execute and not confirm_azure_run:
        blockers.append("--confirm-azure-run is required with --execute")
    if execute and confirm_azure_run and preflight["ready"]:
        status = "ready-to-submit"
    elif execute:
        status = "blocked"
    return {
        "status": status,
        "backend": "azure-ml",
        "run_id": spec.run_id,
        "resource_group": spec.resource_group,
        "workspace": spec.workspace,
        "region": spec.region,
        "compute": spec.compute,
        "job_template": str(spec.job_template),
        "execute": execute,
        "confirm_azure_run": confirm_azure_run,
        "command": command,
        "shell_command": " ".join(shlex.quote(part) for part in command),
        "preflight": preflight,
        "blockers": blockers,
        "claim_boundary": "No-limit benchmark claim only after Azure completes every configured task without --limit and artifacts are downloaded to /Volumes/PortableSSD.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--resource-group", default=DEFAULT_RESOURCE_GROUP)
    parser.add_argument("--workspace", default=DEFAULT_WORKSPACE)
    parser.add_argument("--region", default=DEFAULT_REGION)
    parser.add_argument("--compute", default=DEFAULT_COMPUTE)
    parser.add_argument("--job-template", type=Path, default=DEFAULT_JOB_TEMPLATE)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-azure-run", action="store_true")
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    spec = AzureScorecardSpec(
        run_id=args.run_id,
        resource_group=args.resource_group,
        workspace=args.workspace,
        region=args.region,
        compute=args.compute,
        job_template=args.job_template,
    )
    report = build_report(spec, args.execute, args.confirm_azure_run)

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.execute:
        if not args.confirm_azure_run or report["blockers"]:
            print(json.dumps(report, indent=2, sort_keys=True))
            return 2
        result = subprocess.run(report["command"], check=False, capture_output=True, text=True)
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
