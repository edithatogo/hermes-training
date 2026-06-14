#!/usr/bin/env python3
"""Generate the current cloud backend unblock checklist from preflight state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_PREFLIGHT = Path("reports/cloud/backend-preflight-20260613.json")
DEFAULT_MARKDOWN = Path("reports/cloud/backend-unblock-checklist-20260613.md")
DEFAULT_JSON = Path("reports/cloud/backend-unblock-checklist-20260613.json")
DEFAULT_KAGGLE_CONTRACT = Path("reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.json")
DEFAULT_KAGGLE_INGEST = Path("reports/cloud/qwen3-v4-peft-kaggle-result-ingest-20260614.json")
DEFAULT_KAGGLE_RERUN_STATUS = Path("reports/cloud/qwen3-v4-peft-kaggle-status-rerun-p100-v7-20260614.json")


def load_preflight(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("backends"), dict):
        raise ValueError(f"{path} does not look like a cloud backend preflight report")
    return data


def load_optional_json(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def derive_kaggle_status(
    status: str,
    contract_report: dict[str, Any] | None,
    ingest_report: dict[str, Any] | None,
    rerun_status_report: dict[str, Any] | None = None,
) -> str:
    if status != "prepared-needs-notebook-contract":
        return status
    contract_passed = contract_report is not None and contract_report.get("status") == "pass"
    ingest_ready = ingest_report is not None and ingest_report.get("status") in {"pass", "pending_artifacts"}
    rerun_status = str(rerun_status_report.get("status", "")) if rerun_status_report else ""
    rerun_submitted = rerun_status.startswith("KernelWorkerStatus.")
    if contract_passed and ingest_ready and rerun_status == "KernelWorkerStatus.COMPLETE":
        return "completed-failed-needs-kaggle-runner-fix"
    if contract_passed and ingest_ready and rerun_submitted:
        return "running-needs-artifact-recovery"
    if contract_passed and ingest_ready:
        return "prepared-needs-run-approval"
    return status


def kaggle_unblock_item(status: str) -> dict[str, Any]:
    if status == "prepared-needs-quota-cli-fix-and-notebook-contract":
        return {
            "backend": "kaggle",
            "status": status,
            "blocker": "Kaggle CLI is authenticated, but `kaggle quota` fails before reporting accelerator quota.",
            "operator_actions": [
                "Resolve the Kaggle quota command failure or verify quota through an equivalent non-mutating Kaggle account page/API path.",
                "Review dataset terms and avoid private data uploads.",
                "Push the staged kernel only after explicit confirmation.",
            ],
            "commands": [
                "kaggle quota",
                "kaggle kernels list --mine --page-size 1",
                "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py --execute --confirm-kaggle-run",
            ],
        }
    if status == "prepared-needs-notebook-contract":
        return {
            "backend": "kaggle",
            "status": status,
            "blocker": "Kaggle CLI is authenticated and accelerator quota is visible; remaining gates are dataset terms and a fail-closed notebook/job contract.",
            "operator_actions": [
                "Use the preflight SDK fallback quota evidence while the public `kaggle quota` renderer is failing.",
                "Review dataset terms and avoid private data uploads.",
                "Push the staged kernel only after explicit confirmation.",
            ],
            "commands": [
                "./.venv/bin/python scripts/cloud_backend_preflight.py",
                "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py --execute --confirm-kaggle-run",
            ],
        }
    if status == "prepared-needs-run-approval":
        return {
            "backend": "kaggle",
            "status": status,
            "blocker": "Kaggle CLI, quota visibility, public-input notebook contract, and local result ingest gate are ready; remaining gates are explicit run approval and artifact recovery.",
            "operator_actions": [
                "Confirm the no-limit Kaggle run is approved before pushing the public kernel.",
                "Download `/kaggle/working` summary and lm-eval outputs to the SSD after the run.",
                "Run the result ingest validator with `--no-allow-pending` before any benchmark claim.",
            ],
            "commands": [
                "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py --execute --confirm-kaggle-run",
                "./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json <downloaded-summary> --no-allow-pending",
            ],
        }
    if status == "running-needs-artifact-recovery":
        version = 3
        artifact_dir = "/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v3"
        return {
            "backend": "kaggle",
            "status": status,
            "blocker": f"Kaggle kernel version {version} has been submitted and is running; remaining gate is SSD artifact recovery plus no-pending ingest validation.",
            "operator_actions": [
                "Poll the Kaggle kernel status until it is complete.",
                "Download `/kaggle/working` summary and lm-eval outputs to the SSD artifact directory.",
                "Run the result ingest validator with `--no-allow-pending` before any benchmark claim.",
            ],
            "commands": [
                "kaggle kernels status edithatogo/qwen3-v4-peft-lm-eval-selected-full",
                f"kaggle kernels output edithatogo/qwen3-v4-peft-lm-eval-selected-full --path {artifact_dir}",
                "./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json <downloaded-summary> --no-allow-pending",
            ],
        }
    if status == "completed-failed-needs-kaggle-runner-fix":
        return {
            "backend": "kaggle",
            "status": status,
            "blocker": "Kaggle kernel version 3 completed without scores; the NumPy-pinned runner contract now passes, but any further rerun requires explicit approval or rerouting.",
            "operator_actions": [
                "Keep the recovered v2 and v3 failed summaries on the SSD as non-promotional evidence.",
                "Use the passed staged runner contract as the baseline if another Kaggle rerun is explicitly approved.",
                "Prefer a persistent backend such as Modal if cost/credit policy is cleared.",
            ],
            "commands": [
                "./.venv/bin/python scripts/validate_kaggle_rerun_submit_report.py",
                "./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v2/qwen3-v4-peft-kaggle-lm-eval-20260613-233405-summary.json --no-allow-pending",
                "./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v3/qwen3-v4-peft-kaggle-lm-eval-20260613-234300-summary.json --no-allow-pending",
                "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py",
            ],
        }
    return {
        "backend": "kaggle",
        "status": status,
        "blocker": "Kaggle CLI is installed but unauthenticated.",
        "operator_actions": [
            "Authenticate Kaggle CLI with OAuth or an API token.",
            "Check weekly accelerator quota before pushing a kernel.",
            "Push the staged kernel only after explicit confirmation.",
        ],
        "commands": [
            "kaggle auth login",
            "kaggle quota",
            "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py",
            "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py --execute --confirm-kaggle-run",
        ],
    }


def kaggle_running_unblock_item(rerun_status_report: dict[str, Any]) -> dict[str, Any]:
    version = rerun_status_report.get("kernel_version", "unknown")
    artifact_dir = rerun_status_report.get(
        "artifact_dir",
        "/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v4-20260614",
    )
    return {
        "backend": "kaggle",
        "status": "running-needs-artifact-recovery",
        "blocker": f"Kaggle kernel version {version} has been submitted and is running; remaining gate is SSD artifact recovery plus no-pending ingest validation.",
        "operator_actions": [
            "Poll the Kaggle kernel status until it is complete.",
            "Download `/kaggle/working` summary and lm-eval outputs to the SSD artifact directory.",
            "Run the result ingest validator with `--no-allow-pending` before any benchmark claim.",
        ],
        "commands": [
            "kaggle kernels status edithatogo/qwen3-v4-peft-lm-eval-selected-full",
            f"kaggle kernels output edithatogo/qwen3-v4-peft-lm-eval-selected-full --path {artifact_dir}",
            "./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json <downloaded-summary> --no-allow-pending",
        ],
    }


def kaggle_completed_failed_unblock_item(rerun_status_report: dict[str, Any]) -> dict[str, Any]:
    version = rerun_status_report.get("kernel_version", 3)
    artifact_dir = rerun_status_report.get(
        "artifact_dir",
        "/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v3",
    )
    summary_path = rerun_status_report.get("recovered_summary")
    ingest_command = (
        f"./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json {summary_path} --no-allow-pending"
        if summary_path
        else "./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json <downloaded-summary> --no-allow-pending"
    )
    return {
        "backend": "kaggle",
        "status": "completed-failed-needs-kaggle-runner-fix",
        "blocker": f"Kaggle kernel version {version} completed without scores; the recovered summary is blocked, and this P100 path now needs a runner/runtime change or a different backend.",
        "operator_actions": [
            f"Keep the recovered version {version} failed summary on the SSD as non-promotional evidence.",
            "Do not submit another unchanged P100/CUDA Kaggle rerun.",
            "Prefer a persistent backend such as Modal if cost/credit policy is cleared.",
        ],
        "commands": [
            "./.venv/bin/python scripts/validate_kaggle_rerun_submit_report.py",
            ingest_command,
            f"kaggle kernels output edithatogo/qwen3-v4-peft-lm-eval-selected-full --path {artifact_dir}",
            "./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py",
        ],
    }


def modal_unblock_item(status: str) -> dict[str, Any]:
    if status == "prepared-needs-credit-and-gpu-policy-check":
        return {
            "backend": "modal",
            "status": status,
            "blocker": "Modal CLI is authenticated; remaining gates are free credit/grant proof, GPU policy, and fail-closed result persistence.",
            "operator_actions": [
                "Run the Modal policy gate validator; empty billing is usage evidence only, not zero-cost GPU proof.",
                "Confirm free credits, academic grant, or other zero-cost allowance before GPU execution.",
                "Record non-secret GPU policy evidence for the intended workspace.",
                "Keep the prepared Modal submitter blocked until the policy gate explicitly allows execution.",
            ],
            "commands": [
                "modal profile list",
                "modal billing report --for \"this month\" --json",
                "./.venv/bin/python scripts/validate_modal_policy_gate.py",
                "./.venv/bin/python scripts/submit_modal_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_modal_peft_scorecard.py --execute --confirm-modal-run --confirm-zero-cost-compute",
            ],
        }
    return {
        "backend": "modal",
        "status": status,
        "blocker": "Modal CLI is installed but no token/profile is authenticated on this machine.",
        "operator_actions": [
            "Run browser token setup for the intended Modal account.",
            "Confirm free credits, academic grant, or other zero-cost allowance before GPU execution.",
            "Add a fail-closed Modal scorecard submitter only after auth and result persistence are proven.",
        ],
        "commands": [
            "modal token new",
            "modal token info",
            "modal profile list",
            "modal billing",
        ],
    }


def checklist_items(
    preflight: dict[str, Any],
    kaggle_contract_report: dict[str, Any] | None = None,
    kaggle_ingest_report: dict[str, Any] | None = None,
    kaggle_rerun_status_report: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    backends = preflight["backends"]
    kaggle_status = derive_kaggle_status(
        backends.get("kaggle", {}).get("status", "unknown"),
        kaggle_contract_report,
        kaggle_ingest_report,
        kaggle_rerun_status_report,
    )
    colab_policy = backends.get("colab", {}).get("accelerator_policy", {})
    colab_dispatch_command = colab_policy.get(
        "dispatch_command",
        "./.venv/bin/python scripts/colab_dispatch.py --accelerators gpu:T4,gpu:L4 scripts/colab_smoke.py",
    )
    return [
        {
            "backend": "colab",
            "status": backends.get("colab", {}).get("status", "unknown"),
            "accelerator_policy": colab_policy,
            "blocker": (
                "No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits "
                "HTTP 403 for project 1014160490159."
            ),
            "operator_actions": [
                "Confirm `colab sessions` is empty or intentionally owned.",
                "Use the GPU ladder for PEFT lm-eval scorecards; do not route those scorecards to TPU.",
                "Use `--allow-tpu` only for TPU-compatible adaptive scripts such as `scripts/colab_adaptive_train_smoke.py`.",
                "Fix Google Cloud service usage permission (`serviceusage.services.use`) for project 1014160490159 before another no-limit shard retry.",
                "If that permission cannot be fixed, prefer a persistent backend instead of repeated Colab retries.",
            ],
            "commands": [
                "PATH=\"$HOME/.local/bin:$PATH\" colab sessions",
                "./.venv/bin/python scripts/cloud_backend_preflight.py",
                "# bounded GPU/TPU adaptive smoke, no scorecard claim:",
                colab_dispatch_command,
                "# after permission is fixed:",
                "./.venv/bin/python scripts/colab_lm_eval_shard.py launch --config reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-config-20260613.json --session qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry3 --gpu T4",
            ],
        },
        {
            "backend": "hf_jobs",
            "status": backends.get("hf_jobs", {}).get("status", "unknown"),
            "blocker": "HF Jobs rejected the live route probe with insufficient prepaid credits.",
            "operator_actions": [
                "Add Hugging Face prepaid credits or grant capacity.",
                "Keep paid GPU submission explicitly confirmation-gated.",
                "Submit the prepared scorecard only after credits are visible.",
            ],
            "commands": [
                "hf jobs ps",
                "./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py --execute --confirm-paid-compute",
            ],
        },
        {
            "backend": "azure",
            "status": backends.get("azure", {}).get("status", "unknown"),
            "blocker": "Azure CLI is installed but not currently logged in.",
            "operator_actions": [
                "Run device-code login for the intended account.",
                "Select `Azure for Students` if available.",
                "Rerun quota checks before any workspace, compute, or job action.",
            ],
            "commands": [
                "az login --use-device-code",
                "az account set --subscription \"Azure for Students\"",
                "./.venv/bin/python scripts/azure_preflight.py --check-quota --region australiaeast",
                "./.venv/bin/python scripts/azure_status.py",
                "./.venv/bin/python scripts/submit_azure_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_azure_peft_scorecard.py --execute --confirm-azure-run",
            ],
        },
        {
            "backend": "ngc",
            "status": backends.get("ngc", {}).get("status", "unknown"),
            "blocker": "NGC has no configured API key, SSO session, org/team, GPU quota, or benchmark container.",
            "operator_actions": [
                "Authenticate with SSO or supplied API key without committing secrets.",
                "Record non-secret org/team and Cloud Function GPU quota evidence.",
                "Build or select an NGC registry benchmark container before any task submission.",
            ],
            "commands": [
                "ngc sso login",
                "ngc config current",
                "ngc cloud-function gpu quota",
                "ngc cloud-function task create --help",
                "./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py",
                "./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py --container-image <ngc-registry-image> --gpu-specification <gpu-spec> --execute --confirm-ngc-run",
            ],
        },
        (
            kaggle_running_unblock_item(kaggle_rerun_status_report)
            if kaggle_status == "running-needs-artifact-recovery" and kaggle_rerun_status_report
            else (
                kaggle_completed_failed_unblock_item(kaggle_rerun_status_report)
                if kaggle_status == "completed-failed-needs-kaggle-runner-fix" and kaggle_rerun_status_report
                else kaggle_unblock_item(kaggle_status)
            )
        ),
        modal_unblock_item(backends.get("modal", {}).get("status", "unknown")),
        {
            "backend": "lightning",
            "status": backends.get("lightning", {}).get("status", "unknown"),
            "blocker": "Lightning SDK is installed, but Studio/Job commands need login and a configured Teamspace owner.",
            "operator_actions": [
                "Run Lightning login for the intended account.",
                "Select or configure the Teamspace owner.",
                "Confirm free monthly credits/GPU hours and a T4/L4 machine before adding a submitter.",
            ],
            "commands": [
                "lightning login",
                "lightning studio list",
                "lightning machine list",
                "lightning job list",
                "./.venv/bin/python scripts/submit_lightning_peft_scorecard.py",
                "./.venv/bin/python scripts/submit_lightning_peft_scorecard.py --teamspace <owner>/<teamspace> --execute --confirm-lightning-run --confirm-zero-cost-compute",
            ],
        },
    ]


def render_markdown(items: list[dict[str, Any]], source: Path) -> str:
    lines = [
        "# Cloud Backend Unblock Checklist",
        "",
        f"Source preflight: `{source}`",
        "",
        "This checklist is fail-closed. It records the next operator actions but does not run login, paid compute, or remote jobs.",
        "",
    ]
    for item in items:
        lines.extend(
            [
                f"## {item['backend']}",
                "",
                f"- Status: `{item['status']}`",
                f"- Blocker: {item['blocker']}",
                "- Operator actions:",
            ]
        )
        for action in item["operator_actions"]:
            lines.append(f"  - {action}")
        if item.get("accelerator_policy"):
            policy = item["accelerator_policy"]
            lines.extend(
                [
                    "- Accelerator policy:",
                    f"  - Default ladder: `{policy.get('default_ladder', 'unknown')}`",
                    f"  - TPU requires opt-in: `{policy.get('tpu_requires_opt_in', True)}`",
                    f"  - TPU-compatible scripts: `{', '.join(policy.get('tpu_compatible_scripts', [])) or 'none'}`",
                    f"  - TPU-incompatible workloads: `{', '.join(policy.get('tpu_incompatible_workloads', [])) or 'none'}`",
                ]
            )
        lines.extend(["- Commands:", ""])
        lines.append("```bash")
        lines.extend(item["commands"])
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", type=Path, default=DEFAULT_PREFLIGHT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--kaggle-contract-report", type=Path, default=DEFAULT_KAGGLE_CONTRACT)
    parser.add_argument("--kaggle-ingest-report", type=Path, default=DEFAULT_KAGGLE_INGEST)
    parser.add_argument("--kaggle-rerun-status-report", type=Path, default=DEFAULT_KAGGLE_RERUN_STATUS)
    args = parser.parse_args()

    preflight = load_preflight(args.preflight)
    items = checklist_items(
        preflight,
        load_optional_json(args.kaggle_contract_report),
        load_optional_json(args.kaggle_ingest_report),
        load_optional_json(args.kaggle_rerun_status_report),
    )
    payload = {"source_preflight": str(args.preflight), "items": items}

    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(render_markdown(items, args.preflight), encoding="utf-8")
    args.json_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
