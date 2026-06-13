#!/usr/bin/env python3
"""Probe whether the published MLX LoRA adapter can run on Colab.

This is a portability/blocker probe for the Qwen3 v4 full scorecard. It does
not run lm-eval and it does not download base model weights.
"""
from __future__ import annotations

import importlib
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ADAPTER_REPO = "edithatogo/qwen3-4b-hermes-lora"
EXPECTED_FILES = {"adapter_config.json", "adapters.safetensors", "README.md"}


def run_command(command: list[str], timeout_s: int) -> dict[str, Any]:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=timeout_s)
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": None,
            "timed_out": True,
            "stdout_tail": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
        }
    return {
        "command": command,
        "returncode": result.returncode,
        "timed_out": False,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def import_status(module: str) -> dict[str, str]:
    try:
        imported = importlib.import_module(module)
    except Exception as exc:  # noqa: BLE001
        return {"status": "blocked", "error": f"{type(exc).__name__}: {exc}"}
    return {"status": "ok", "version": getattr(imported, "__version__", "unknown")}


def runtime_details() -> dict[str, Any]:
    details: dict[str, Any] = {
        "created_at": datetime.now(UTC).isoformat(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
    }
    try:
        import torch

        details["torch"] = getattr(torch, "__version__", "unknown")
        details["cuda_available"] = bool(torch.cuda.is_available())
        details["cuda_device_name"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    except Exception as exc:  # noqa: BLE001
        details["torch_error"] = f"{type(exc).__name__}: {exc}"
        details["cuda_available"] = False
        details["cuda_device_name"] = None
    return details


def list_adapter_files() -> dict[str, Any]:
    try:
        from huggingface_hub import HfApi

        info = HfApi().model_info(ADAPTER_REPO, files_metadata=True)
    except Exception as exc:  # noqa: BLE001
        return {"status": "blocked", "error": f"{type(exc).__name__}: {exc}"}
    files = sorted(sibling.rfilename for sibling in info.siblings)
    return {
        "status": "ok",
        "repo": info.id,
        "private": info.private,
        "sha": info.sha,
        "files": files,
        "expected_files_present": sorted(EXPECTED_FILES.intersection(files)),
        "missing_expected_files": sorted(EXPECTED_FILES.difference(files)),
    }


def main() -> int:
    pip_install = run_command([sys.executable, "-m", "pip", "install", "--quiet", "huggingface_hub", "safetensors"], 120)
    mlx_install = run_command([sys.executable, "-m", "pip", "install", "--quiet", "mlx-lm"], 180)
    adapter = list_adapter_files()
    imports = {
        "huggingface_hub": import_status("huggingface_hub"),
        "safetensors": import_status("safetensors"),
        "mlx": import_status("mlx"),
        "mlx_lm": import_status("mlx_lm"),
    }
    mlx_ready = imports["mlx"]["status"] == "ok" and imports["mlx_lm"]["status"] == "ok"
    adapter_visible = adapter.get("status") == "ok" and not adapter.get("missing_expected_files")
    result = {
        "status": "scored" if mlx_ready and adapter_visible else "blocked",
        "probe": "colab-mlx-adapter-portability",
        "claim_boundary": "Portability probe only; no benchmark score and no model inference.",
        "runtime": runtime_details(),
        "pip_install": pip_install,
        "mlx_lm_install": mlx_install,
        "adapter": adapter,
        "imports": imports,
        "decision": (
            "The published adapter is visible and MLX imports on this Colab runtime."
            if mlx_ready and adapter_visible
            else "The published adapter is visible, but the MLX adapter path is not a CUDA/T4 lm-eval path; use a PEFT/fused artifact or a Mac/MLX runner."
            if adapter_visible
            else "The adapter repo or expected files were not accessible from Colab."
        ),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    output = Path("colab_mlx_adapter_portability_probe.json")
    output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
