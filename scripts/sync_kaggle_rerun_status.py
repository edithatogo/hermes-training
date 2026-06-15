#!/usr/bin/env python3
"""Sync Kaggle rerun status and optionally recover completed artifacts to SSD."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KERNEL_ID = "edithatogo/qwen3-v4-peft-lm-eval-selected-full"
DEFAULT_VERSION = 7
DEFAULT_ARTIFACT_DIR = Path("/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v7-20260614")
DEFAULT_JSON = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-status-rerun-p100-v7-20260614.json"
DEFAULT_MARKDOWN = ROOT / "reports/cloud/qwen3-v4-peft-kaggle-status-rerun-p100-v7-20260614.md"


def run_command(command: list[str], timeout_s: int = 600) -> dict[str, Any]:
    result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=timeout_s)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def parse_status(stdout: str) -> str:
    marker = 'status "'
    if marker not in stdout:
        return "unknown"
    return stdout.split(marker, 1)[1].split('"', 1)[0]


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def find_summary(path: Path) -> str | None:
    if not path.exists():
        return None
    candidates = sorted(path.glob("*summary.json"))
    return str(candidates[0]) if candidates else None


def read_summary_status(path: str | None) -> str | None:
    if not path:
        return None
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if isinstance(data, dict):
        status = data.get("status")
        return str(status) if status is not None else None
    return None


def build_status_report(
    *,
    kernel_id: str,
    kernel_version: int,
    artifact_dir: Path,
    status_result: dict[str, Any],
    download_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    status = parse_status(str(status_result.get("stdout", "")))
    downloaded_file_count = count_files(artifact_dir)
    recovered_summary = find_summary(artifact_dir)
    recovered_summary_status = read_summary_status(recovered_summary)
    base = {
        "kernel_id": kernel_id,
        "kernel_version": kernel_version,
        "status": status,
        "status_stdout": status_result.get("stdout", ""),
        "command": status_result.get("command", ["kaggle", "kernels", "status", kernel_id]),
        "artifact_dir": str(artifact_dir),
        "download_command": ["kaggle", "kernels", "output", kernel_id, "--path", str(artifact_dir)],
        "downloaded_file_count": downloaded_file_count,
        "recovered_summary": recovered_summary,
        "recovered_summary_status": recovered_summary_status,
        "download_result": download_result,
    }
    if status == "KernelWorkerStatus.COMPLETE":
        if recovered_summary_status == "scored":
            outcome_summary = (
                "Kernel completed with status=scored; recovered artifacts must still pass the no-pending ingest "
                "validator before any benchmark claim."
            )
        elif recovered_summary_status:
            outcome_summary = (
                f"Kernel completed with status={recovered_summary_status}; run no-pending ingest validation "
                "before any claim."
            )
        elif recovered_summary is not None:
            outcome_summary = "Kernel completed and a summary was recovered; run no-pending ingest validation before any claim."
        else:
            outcome_summary = (
                "Kernel completed. Artifacts must be recovered to the SSD and validated before any scored or "
                "blocked outcome can be promoted."
            )
        base.update(
            {
                "claim_boundary": (
                    "No benchmark claim until recovered artifacts pass the no-pending Kaggle result ingest validator."
                ),
                "failure_summary": outcome_summary,
            }
        )
    elif status == "KernelWorkerStatus.RUNNING":
        base.update(
            {
                "claim_boundary": (
                    "No benchmark claim: Kaggle kernel is still running, and no complete artifact set has been validated."
                ),
                "running_summary": (
                    "Kernel is running. Remaining gates are artifact recovery to the SSD and no-pending ingest validation "
                    "before any benchmark claim."
                ),
            }
        )
    else:
        base.update(
            {
                "claim_boundary": "No benchmark claim: Kaggle kernel status is not a validated scored outcome.",
                "failure_summary": f"Kaggle status is {status}; inspect kernel logs and recovered artifacts before rerouting.",
            }
        )
    return base


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 V4 PEFT Kaggle P100 Rerun Status",
        "",
        f"Status: `{report['status']}`",
        "",
        f"Kernel: `{report['kernel_id']}`",
        "",
        f"Kernel version: `{report['kernel_version']}`",
        "",
        f"Artifact directory: `{report['artifact_dir']}`",
        "",
        f"Downloaded files: `{report['downloaded_file_count']}`",
        "",
    ]
    if report.get("recovered_summary"):
        lines.extend(["Recovered summary:", f"`{report['recovered_summary']}`", ""])
    lines.extend(["## Claim Boundary", "", report["claim_boundary"], ""])
    if report.get("running_summary"):
        lines.extend(["## Running Summary", "", report["running_summary"], ""])
    if report.get("failure_summary"):
        lines.extend(["## Failure Summary", "", report["failure_summary"], ""])
    if report.get("download_result") is not None:
        download = report["download_result"]
        lines.extend(
            [
                "## Download Result",
                "",
                f"- Return code: `{download.get('returncode')}`",
                f"- Stdout: `{download.get('stdout', '')}`",
                f"- Stderr: `{download.get('stderr', '')}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Evidence",
            "",
            "`kaggle kernels status {}` reported:".format(report["kernel_id"]),
            "",
            f"`{report['status_stdout']}`",
            "",
        ]
    )
    return "\n".join(lines)


def sync_status(
    *,
    kernel_id: str,
    kernel_version: int,
    artifact_dir: Path,
    recover_artifacts: bool,
) -> dict[str, Any]:
    status_result = run_command(["kaggle", "kernels", "status", kernel_id], timeout_s=120)
    download_result = None
    status = parse_status(str(status_result.get("stdout", "")))
    if recover_artifacts and status == "KernelWorkerStatus.COMPLETE":
        artifact_dir.mkdir(parents=True, exist_ok=True)
        download_result = run_command(["kaggle", "kernels", "output", kernel_id, "--path", str(artifact_dir)], timeout_s=1800)
    return build_status_report(
        kernel_id=kernel_id,
        kernel_version=kernel_version,
        artifact_dir=artifact_dir,
        status_result=status_result,
        download_result=download_result,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kernel-id", default=DEFAULT_KERNEL_ID)
    parser.add_argument("--kernel-version", type=int, default=DEFAULT_VERSION)
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--recover-artifacts", action="store_true")
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    report = sync_status(
        kernel_id=args.kernel_id,
        kernel_version=args.kernel_version,
        artifact_dir=args.artifact_dir,
        recover_artifacts=args.recover_artifacts,
    )
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] in {"KernelWorkerStatus.RUNNING", "KernelWorkerStatus.COMPLETE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
