#!/usr/bin/env python3
"""Read-only cloud backend preflight registry for benchmark orchestration.

The script records provider readiness without creating sessions, logging in,
creating cloud resources, uploading data, or submitting jobs. It returns success
when the registry can be written, even if individual providers are blocked.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def resolve_storage_root() -> Path:
    if os.environ.get("HERMES_STORAGE_ROOT"):
        return Path(os.environ["HERMES_STORAGE_ROOT"])
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD")
    return Path.cwd() / ".local-storage"


def run_command(command: list[str], timeout_s: int = 30) -> dict[str, Any]:
    executable = shutil.which(command[0])
    if not executable:
        return {
            "installed": False,
            "path": "",
            "command": command,
            "returncode": None,
            "stdout": "",
            "stderr": f"{command[0]} not found on PATH",
        }
    try:
        result = subprocess.run(
            [executable, *command[1:]],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
    except Exception as exc:  # noqa: BLE001
        return {
            "installed": True,
            "path": executable,
            "command": command,
            "returncode": None,
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
        }
    return {
        "installed": True,
        "path": executable,
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def summarize_colab() -> dict[str, Any]:
    version = run_command(["colab", "version"])
    sessions = run_command(["colab", "sessions"])
    ready = version["installed"] and version["returncode"] == 0 and sessions["returncode"] == 0
    return {
        "status": "ready" if ready else "blocked",
        "route": "primary",
        "version": version,
        "sessions": sessions,
        "stop_condition": "no Colab CLI, command failure, active session not intentionally owned, or upload requires private data",
        "next_action": "Use scripts/colab_dispatch.py for bounded GPU-first jobs; update google-colab-cli when convenient.",
    }


def summarize_azure() -> dict[str, Any]:
    account = run_command(["az", "account", "show", "-o", "json"])
    status = "blocked"
    detail = "Azure CLI not installed"
    if account["installed"] and account["returncode"] == 0:
        status = "prepared-needs-quota-check"
        detail = "active account present; run scripts/azure_preflight.py --check-quota before compute"
    elif account["installed"]:
        detail = account["stderr"] or account["stdout"] or "az account show failed"
    return {
        "status": status,
        "route": "prepared",
        "account": account,
        "detail": detail,
        "stop_condition": "missing login, wrong subscription, absent Azure ML extension, zero GPU quota, or no cost approval",
        "next_action": "Run az login only when the user is ready; then use scripts/azure_preflight.py before any job.",
    }


def summarize_hf_jobs() -> dict[str, Any]:
    whoami = run_command(["hf", "auth", "whoami"])
    hardware = run_command(["hf", "jobs", "hardware"], timeout_s=60)
    jobs = run_command(["hf", "jobs", "ps"])
    ready = (
        whoami["installed"]
        and whoami["returncode"] == 0
        and hardware["returncode"] == 0
        and "t4-small" in hardware["stdout"]
    )
    return {
        "status": "prepared-needs-paid-compute-approval" if ready else "blocked",
        "route": "persistent",
        "whoami": whoami,
        "hardware": hardware,
        "jobs": jobs,
        "stop_condition": "missing HF login, unavailable Jobs hardware, absent mounted artifacts, no result persistence, or no paid compute approval",
        "next_action": "Use HF Jobs for persistent no-limit scorecards only after explicit paid GPU approval.",
    }


def summarize_ngc() -> dict[str, Any]:
    config = run_command(["ngc", "config", "current"])
    configured = config["installed"] and config["returncode"] == 0 and "apikey" in config["stdout"].lower()
    return {
        "status": "prepared-needs-entitlement-check" if configured else "blocked",
        "route": "prepared",
        "config": config,
        "stop_condition": "missing API key, org/team, entitlement, container access, model access, or license approval",
        "next_action": "Configure NGC only after the user supplies keys; record non-secret org/team and entitlement proof.",
    }


def summarize_kaggle() -> dict[str, Any]:
    version = run_command(["kaggle", "--version"])
    return {
        "status": "prepared-needs-auth-check" if version["installed"] and version["returncode"] == 0 else "blocked",
        "route": "future",
        "version": version,
        "stop_condition": "missing CLI, missing credentials, dataset terms, private data, or unbounded notebook runtime",
        "next_action": "Install and authenticate Kaggle CLI before adding Kaggle execution jobs.",
    }


def build_report() -> dict[str, Any]:
    storage_root = resolve_storage_root()
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "storage_root": str(storage_root),
        "storage_root_exists": storage_root.exists(),
        "policy": {
            "no_paid_compute_without_approval": True,
            "no_private_data_uploads": True,
            "no_model_or_dataset_publication": True,
            "artifact_root": str(storage_root / "hermes-evals"),
            "tracked_report_root": "reports/cloud",
        },
        "backends": {
            "colab": summarize_colab(),
            "hf_jobs": summarize_hf_jobs(),
            "azure": summarize_azure(),
            "ngc": summarize_ngc(),
            "kaggle": summarize_kaggle(),
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Cloud Backend Preflight Registry",
        "",
        f"Date: {report['created_at']}",
        f"Storage root: `{report['storage_root']}`",
        f"Storage root exists: `{report['storage_root_exists']}`",
        "",
        "## Policy",
        "",
    ]
    for key, value in report["policy"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Backends",
            "",
            "| Backend | Status | Route | Stop condition | Next action |",
            "|---|---|---|---|---|",
        ]
    )
    for name, backend in report["backends"].items():
        lines.append(
            "| `{name}` | `{status}` | `{route}` | {stop} | {next_action} |".format(
                name=name,
                status=backend["status"],
                route=backend["route"],
                stop=backend["stop_condition"],
                next_action=backend["next_action"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-output", type=Path, default=Path("reports/cloud/backend-preflight-20260612.json"))
    parser.add_argument("--markdown-output", type=Path, default=Path("reports/cloud/backend-preflight-20260612.md"))
    args = parser.parse_args()

    report = build_report()
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
