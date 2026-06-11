#!/usr/bin/env python3
"""Minimal Colab accelerator smoke script.

This script is intended to run remotely through `colab run`. It prints a JSON
report to stdout so the local caller can save the run card under the SSD eval
root.
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def command_output(command: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=20)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "command": command, "error": f"{type(exc).__name__}: {exc}"}
    return {
        "ok": result.returncode == 0,
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def torch_report() -> dict[str, Any]:
    try:
        import torch
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "error": f"{type(exc).__name__}: {exc}"}
    report: dict[str, Any] = {
        "available": True,
        "version": getattr(torch, "__version__", ""),
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
    }
    if torch.cuda.is_available():
        report["cuda_device_name"] = torch.cuda.get_device_name(0)
        report["cuda_capability"] = ".".join(str(part) for part in torch.cuda.get_device_capability(0))
    return report


def tpu_report() -> dict[str, Any]:
    env_keys = ["COLAB_TPU_ADDR", "TPU_NAME", "TPU_WORKER_ID", "TPU_WORKER_HOSTNAMES"]
    report: dict[str, Any] = {key: os.environ.get(key, "") for key in env_keys if os.environ.get(key)}
    try:
        import torch_xla.core.xla_model as xm  # type: ignore[import-not-found]
    except Exception as exc:  # noqa: BLE001
        report["torch_xla_available"] = False
        report["torch_xla_error"] = f"{type(exc).__name__}: {exc}"
        return report
    report["torch_xla_available"] = True
    try:
        report["xla_device"] = str(xm.xla_device())
    except Exception as exc:  # noqa: BLE001
        report["xla_device_error"] = f"{type(exc).__name__}: {exc}"
    return report


def main() -> int:
    report = {
        "created_at": datetime.now(UTC).isoformat(),
        "argv": sys.argv,
        "cwd": str(Path.cwd()),
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch_report(),
        "tpu": tpu_report(),
        "nvidia_smi": command_output(["nvidia-smi"]),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
