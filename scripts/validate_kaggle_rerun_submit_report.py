#!/usr/bin/env python3
"""Validate the Kaggle P100-compatible rerun submission report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-submit-rerun-p100-20260614.json"
DEFAULT_STATUS_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-status-rerun-p100-20260614.json"
DEFAULT_V3_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-submit-rerun-p100-v3-20260614.json"
DEFAULT_V3_STATUS_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-status-rerun-p100-v3-20260614.json"
DEFAULT_V4_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-submit-rerun-p100-v4-20260614.json"
DEFAULT_V4_STATUS_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-status-rerun-p100-v4-20260614.json"
DEFAULT_V5_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-submit-rerun-p100-v5-20260614.json"
DEFAULT_V5_STATUS_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-status-rerun-p100-v5-20260614.json"
DEFAULT_V6_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-submit-rerun-p100-v6-20260614.json"
DEFAULT_V6_STATUS_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-status-rerun-p100-v6-20260614.json"
DEFAULT_V7_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-submit-rerun-p100-v7-20260614.json"
DEFAULT_V7_STATUS_REPORT = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-status-rerun-p100-v7-20260614.json"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def validate_report(path: Path = DEFAULT_REPORT, expected_kernel_version: int = 2) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {display_path(path)}"]
    data = load_json(path)
    if data.get("backend") != "kaggle-kernels":
        failures.append("rerun report must target kaggle-kernels")
    if data.get("execute") is not True or data.get("confirm_kaggle_run") is not True:
        failures.append("rerun report must record explicit execute and confirmation flags")
    if data.get("status") != "ready-to-submit":
        failures.append("rerun report must preserve guarded ready-to-submit status")
    if data.get("torch_compatibility_policy") != "p100-cu118":
        failures.append("rerun report must use the p100-cu118 torch policy")
    if data.get("use_4bit") is not False:
        failures.append("rerun report must disable 4-bit/bitsandbytes for the P100 path")
    if data.get("blockers") != []:
        failures.append("rerun report must have no submitter blockers after explicit confirmation")
    submission = data.get("submission", {})
    if not isinstance(submission, dict):
        failures.append("rerun report must include a submission object")
    else:
        if submission.get("returncode") != 0:
            failures.append("Kaggle rerun submission must have returncode 0")
        stdout = str(submission.get("stdout", ""))
        if f"Kernel version {expected_kernel_version} successfully pushed" not in stdout:
            failures.append(f"Kaggle rerun submission must record kernel version {expected_kernel_version}")
    boundary = str(data.get("claim_boundary", ""))
    if "No-limit benchmark claim only after Kaggle completes" not in boundary:
        failures.append("rerun report must preserve non-promotional claim boundary")
    return failures


def validate_v3_report(path: Path = DEFAULT_V3_REPORT) -> list[str]:
    return validate_report(path, expected_kernel_version=3)


def validate_v4_report(path: Path = DEFAULT_V4_REPORT) -> list[str]:
    return validate_report(path, expected_kernel_version=4)


def validate_v5_report(path: Path = DEFAULT_V5_REPORT) -> list[str]:
    return validate_report(path, expected_kernel_version=5)


def validate_v6_report(path: Path = DEFAULT_V6_REPORT) -> list[str]:
    return validate_report(path, expected_kernel_version=6)


def validate_v7_report(path: Path = DEFAULT_V7_REPORT) -> list[str]:
    return validate_report(path, expected_kernel_version=7)


def validate_status_report(path: Path = DEFAULT_STATUS_REPORT) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {display_path(path)}"]
    data = load_json(path)
    if data.get("kernel_id") != "edithatogo/qwen3-v4-peft-lm-eval-selected-full":
        failures.append("status report must target the Qwen3 v4 PEFT Kaggle kernel")
    if data.get("status") != "KernelWorkerStatus.COMPLETE":
        failures.append("status report must record the current Kaggle COMPLETE state")
    if data.get("downloaded_file_count") != 9:
        failures.append("complete status report must record the recovered file count")
    if data.get("artifact_dir") != "/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v2":
        failures.append("status report must keep kernel-v2 artifacts on the SSD")
    boundary = str(data.get("claim_boundary", ""))
    if "No benchmark claim" not in boundary or "no lm-eval result files" not in boundary:
        failures.append("status report must preserve the non-promotional claim boundary")
    failure_summary = str(data.get("failure_summary", ""))
    for expected in ("status=blocked", "evaluation.returncode=1", "result_files=[]", "use_4bit=true"):
        if expected not in failure_summary:
            failures.append(f"status report failure summary must mention {expected}")
    return failures


def validate_v3_status_report(path: Path = DEFAULT_V3_STATUS_REPORT) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {display_path(path)}"]
    data = load_json(path)
    if data.get("kernel_id") != "edithatogo/qwen3-v4-peft-lm-eval-selected-full":
        failures.append("v3 status report must target the Qwen3 v4 PEFT Kaggle kernel")
    if data.get("status") != "KernelWorkerStatus.COMPLETE":
        failures.append("v3 status report must record the current Kaggle COMPLETE state")
    if data.get("downloaded_file_count") != 9:
        failures.append("v3 complete status report must record the recovered file count")
    if data.get("artifact_dir") != "/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v3":
        failures.append("v3 status report must keep kernel-v3 artifacts on the SSD")
    boundary = str(data.get("claim_boundary", ""))
    if "No benchmark claim" not in boundary or "no lm-eval result files" not in boundary:
        failures.append("v3 status report must preserve the non-promotional claim boundary")
    failure_summary = str(data.get("failure_summary", ""))
    for expected in ("status=blocked", "evaluation.returncode=1", "result_files=[]", "use_4bit=false", "torch=2.2.2+cu118"):
        if expected not in failure_summary:
            failures.append(f"v3 status report failure summary must mention {expected}")
    return failures


def validate_v4_status_report(path: Path = DEFAULT_V4_STATUS_REPORT) -> list[str]:
    return validate_versioned_status_report(path, expected_kernel_version=4)


def validate_v5_status_report(path: Path = DEFAULT_V5_STATUS_REPORT) -> list[str]:
    return validate_versioned_status_report(path, expected_kernel_version=5)


def validate_v6_status_report(path: Path = DEFAULT_V6_STATUS_REPORT) -> list[str]:
    failures = validate_versioned_status_report(path, expected_kernel_version=6)
    if failures:
        return failures
    data = load_json(path)
    failure_summary = str(data.get("failure_summary", ""))
    lower_failure_summary = failure_summary.lower()
    for expected in ("qwen3", "torchao", "torch._C.Tag.needs_fixed_stride_order", "torch==2.2.2+cu118"):
        haystack = lower_failure_summary if expected == "qwen3" else failure_summary
        if expected not in haystack:
            failures.append(f"v6 status report failure summary must mention {expected}")
    return failures


def validate_v7_status_report(path: Path = DEFAULT_V7_STATUS_REPORT) -> list[str]:
    return validate_versioned_status_report(path, expected_kernel_version=7)


def validate_versioned_status_report(path: Path, expected_kernel_version: int) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"missing {display_path(path)}"]
    data = load_json(path)
    if data.get("kernel_id") != "edithatogo/qwen3-v4-peft-lm-eval-selected-full":
        failures.append(f"v{expected_kernel_version} status report must target the Qwen3 v4 PEFT Kaggle kernel")
    if data.get("kernel_version") != expected_kernel_version:
        failures.append(f"v{expected_kernel_version} status report must record kernel version {expected_kernel_version}")
    status = data.get("status")
    if status not in {"KernelWorkerStatus.RUNNING", "KernelWorkerStatus.COMPLETE"}:
        failures.append(f"v{expected_kernel_version} status report must record a live Kaggle RUNNING or COMPLETE state")
    artifact_dir = str(data.get("artifact_dir", ""))
    if not artifact_dir.startswith("/Volumes/PortableSSD/hermes-evals/kaggle/"):
        failures.append(f"v{expected_kernel_version} status report must keep artifacts on the SSD")
    boundary = str(data.get("claim_boundary", ""))
    if "No benchmark claim" not in boundary:
        failures.append(f"v{expected_kernel_version} status report must preserve the non-promotional claim boundary")
    if status == "KernelWorkerStatus.RUNNING":
        if data.get("downloaded_file_count") != 0:
            failures.append(f"running v{expected_kernel_version} status report must not claim downloaded artifacts")
        running_summary = str(data.get("running_summary", ""))
        if "artifact recovery" not in running_summary or "no-pending ingest" not in running_summary:
            failures.append(
                f"running v{expected_kernel_version} status report must name artifact recovery and no-pending ingest gates"
            )
    else:
        if not isinstance(data.get("downloaded_file_count"), int) or data.get("downloaded_file_count") <= 0:
            failures.append(f"complete v{expected_kernel_version} status report must record a positive recovered file count")
        failure_summary = str(data.get("failure_summary", ""))
        if "status=blocked" not in failure_summary and "scored" not in failure_summary:
            failures.append(f"complete v{expected_kernel_version} status report must summarize scored or blocked outcome")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    failures = validate_report(args.report)
    failures.extend(validate_status_report())
    failures.extend(validate_v3_report())
    failures.extend(validate_v3_status_report())
    failures.extend(validate_v4_report())
    failures.extend(validate_v4_status_report())
    failures.extend(validate_v5_report())
    failures.extend(validate_v5_status_report())
    failures.extend(validate_v6_report())
    failures.extend(validate_v6_status_report())
    failures.extend(validate_v7_report())
    failures.extend(validate_v7_status_report())
    if failures:
        print("not ready: Kaggle P100 rerun submit report")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: Kaggle P100 rerun submit report is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
