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

HF_JOBS_SCORECARD_REPORT = Path("reports/cloud/qwen3-v4-peft-hf-jobs-scorecard-plan-20260613.md")


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
    credit_blocker_observed = False
    if HF_JOBS_SCORECARD_REPORT.exists():
        report_text = HF_JOBS_SCORECARD_REPORT.read_text(encoding="utf-8")
        credit_blocker_observed = "402 Payment Required" in report_text or "Pre-paid credit balance is insufficient" in report_text
    ready = (
        whoami["installed"]
        and whoami["returncode"] == 0
        and hardware["returncode"] == 0
        and "t4-small" in hardware["stdout"]
    )
    status = "blocked-insufficient-hf-credits" if ready and credit_blocker_observed else "prepared-needs-paid-compute-approval"
    return {
        "status": status if ready else "blocked",
        "route": "persistent",
        "whoami": whoami,
        "hardware": hardware,
        "jobs": jobs,
        "credit_blocker_observed": credit_blocker_observed,
        "stop_condition": "missing HF login, unavailable Jobs hardware, absent mounted artifacts, no result persistence, or no paid compute approval",
        "next_action": (
            "Add HF prepaid credits or grant capacity, then submit with "
            "scripts/submit_hf_jobs_peft_scorecard.py --execute --confirm-paid-compute."
            if credit_blocker_observed
            else "Use HF Jobs for persistent no-limit scorecards only after explicit paid GPU approval."
        ),
    }


def summarize_ngc() -> dict[str, Any]:
    config = run_command(["ngc", "config", "current"])
    configured = config["installed"] and config["returncode"] == 0 and "apikey" in config["stdout"].lower()
    return {
        "status": "prepared-needs-entitlement-check" if configured else "blocked",
        "route": "prepared",
        "config": config,
        "stop_condition": "missing API key, org/team, entitlement, container access, model access, or license approval",
        "next_action": "Configure NGC only after the user supplies keys or completes SSO; then check Cloud Function GPU quota and registry access.",
    }


def summarize_kaggle() -> dict[str, Any]:
    version = run_command(["kaggle", "--version"])
    config = run_command(["kaggle", "config", "view"]) if version["installed"] else {
        "installed": False,
        "path": "",
        "command": ["kaggle", "config", "view"],
        "returncode": None,
        "stdout": "",
        "stderr": "kaggle not found on PATH",
    }
    authenticated = version["installed"] and version["returncode"] == 0 and config["returncode"] == 0
    if authenticated:
        status = "prepared-needs-notebook-contract"
        next_action = "Add a fail-closed Kaggle notebook/job spec and dry-run it before any public dataset or GPU execution."
    elif version["installed"] and version["returncode"] == 0:
        status = "blocked-needs-auth"
        next_action = "Authenticate Kaggle CLI with kaggle auth login or API token, then rerun this preflight."
    else:
        status = "blocked"
        next_action = "Install and authenticate Kaggle CLI before adding Kaggle execution jobs."
    return {
        "status": status,
        "route": "future",
        "version": version,
        "config": config,
        "stop_condition": "missing CLI, missing credentials, dataset terms, private data, or unbounded notebook runtime",
        "next_action": next_action,
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
            "no_unreviewed_model_or_dataset_publication": True,
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


def without_created_at(report: dict[str, Any]) -> dict[str, Any]:
    comparable = dict(report)
    comparable.pop("created_at", None)
    return comparable


def write_if_meaningfully_changed(path: Path, content: str, *, existing_equivalent: bool = False) -> bool:
    if existing_equivalent and path.exists():
        return False
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def write_outputs(report: dict[str, Any], json_output: Path, markdown_output: Path) -> dict[str, bool]:
    existing_equivalent = False
    if json_output.exists():
        try:
            existing = json.loads(json_output.read_text(encoding="utf-8"))
            existing_equivalent = without_created_at(existing) == without_created_at(report)
        except json.JSONDecodeError:
            existing_equivalent = False

    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    return {
        "json": write_if_meaningfully_changed(
            json_output,
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            existing_equivalent=existing_equivalent,
        ),
        "markdown": write_if_meaningfully_changed(
            markdown_output,
            render_markdown(report),
            existing_equivalent=existing_equivalent,
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-output", type=Path, default=Path("reports/cloud/backend-preflight-20260613.json"))
    parser.add_argument("--markdown-output", type=Path, default=Path("reports/cloud/backend-preflight-20260613.md"))
    args = parser.parse_args()

    report = build_report()
    write_outputs(report, args.json_output, args.markdown_output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
