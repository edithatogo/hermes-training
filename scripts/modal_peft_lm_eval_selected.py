#!/usr/bin/env python3
"""Modal app for the Qwen3 v4 PEFT lm-eval selected scorecard.

This module defines a Modal function but does not submit work by itself. Use
`scripts/submit_modal_peft_scorecard.py` for the guarded local entrypoint.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import modal


DEFAULT_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"
APP_NAME = "qwen3-v4-peft-lm-eval-selected"
VOLUME_NAME = "qwen3-v4-peft-scorecards"

app = modal.App(APP_NAME)
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "lm_eval[hf]",
    "transformers>=4.56,<5",
    "peft",
    "bitsandbytes",
    "safetensors",
    "accelerate",
    "huggingface_hub",
)
results_volume = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)


def optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    if text in {"", "none", "None", "null", "NULL"}:
        return None
    return text


def run_command(command: list[str], timeout_s: int) -> dict[str, Any]:
    started = time.time()
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=timeout_s)
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": None,
            "timed_out": True,
            "duration_s": time.time() - started,
            "stdout_tail": (exc.stdout or "")[-8000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-8000:] if isinstance(exc.stderr, str) else "",
        }
    return {
        "command": command,
        "returncode": result.returncode,
        "timed_out": False,
        "duration_s": time.time() - started,
        "stdout_tail": result.stdout[-8000:],
        "stderr_tail": result.stderr[-8000:],
    }


def runtime_details() -> dict[str, Any]:
    details: dict[str, Any] = {"created_at": datetime.now(UTC).isoformat(), "python": sys.version.split()[0]}
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


def collect_files(root: Path) -> list[str]:
    if not root.exists():
        return []
    return sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file())


def download_adapter(adapter_repo: str, adapter_dir: Path) -> dict[str, Any]:
    try:
        from huggingface_hub import snapshot_download

        adapter_dir.mkdir(parents=True, exist_ok=True)
        local_path = snapshot_download(repo_id=adapter_repo, local_dir=str(adapter_dir), local_dir_use_symlinks=False)
        return {"status": "downloaded", "repo_id": adapter_repo, "path": local_path}
    except Exception as exc:  # noqa: BLE001
        return {"status": "blocked", "repo_id": adapter_repo, "error": f"{type(exc).__name__}: {exc}"}


@app.function(image=image, gpu="T4", timeout=21600, volumes={"/results": results_volume})
def scorecard(config_json: str) -> str:
    config = json.loads(config_json)
    run_id = str(config.get("run_id", f"qwen3-v4-peft-modal-lm-eval-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"))
    adapter_repo = str(config.get("adapter_repo", "edithatogo/qwen3-4b-hermes-lora-peft-converted"))
    adapter_dir = Path(str(config.get("adapter_dir", "/tmp/qwen3-v4-peft-adapter")))
    base_model = str(config.get("base_model", "Qwen/Qwen3-4B"))
    tasks = str(config.get("tasks", DEFAULT_TASKS))
    limit = optional_text(config.get("limit"))
    batch_size = str(config.get("batch_size", "1"))
    dtype = str(config.get("dtype", "float16"))
    timeout_s = int(config.get("timeout_s", 21600))
    output_dir = Path(str(config.get("output_dir", f"/results/{run_id}/lm-eval-output")))
    result_json = Path(str(config.get("result_json", f"/results/{run_id}/summary.json")))

    result: dict[str, Any] = {
        "status": "blocked",
        "probe": "modal-peft-lm-eval-selected",
        "run_id": run_id,
        "claim_boundary": "No-limit benchmark claim only if every configured task completes without --limit.",
        "adapter_repo": adapter_repo,
        "adapter_dir": str(adapter_dir),
        "base_model": base_model,
        "tasks": tasks,
        "limit": limit,
        "batch_size": batch_size,
        "dtype": dtype,
        "output_dir": str(output_dir),
        "result_json": str(result_json),
        "runtime": runtime_details(),
    }

    try:
        adapter_download = download_adapter(adapter_repo, adapter_dir)
        result["adapter_download"] = adapter_download
        if adapter_download["status"] != "downloaded":
            raise RuntimeError("adapter download failed")
        output_dir.mkdir(parents=True, exist_ok=True)
        result_json.parent.mkdir(parents=True, exist_ok=True)
        model_arg_parts = [
            f"pretrained={base_model}",
            f"peft={adapter_dir}",
            "device_map=auto",
            f"dtype={dtype}",
            "trust_remote_code=True",
            "load_in_4bit=True",
            f"bnb_4bit_compute_dtype={dtype}",
        ]
        command = [
            sys.executable,
            "-m",
            "lm_eval",
            "--model",
            "hf",
            "--model_args",
            ",".join(model_arg_parts),
            "--tasks",
            tasks,
            "--batch_size",
            batch_size,
            "--output_path",
            str(output_dir),
        ]
        if limit is not None:
            command[command.index("--batch_size"):command.index("--batch_size")] = ["--limit", limit]
        evaluation = run_command(command, timeout_s=timeout_s)
        result["evaluation"] = evaluation
        result["result_files"] = collect_files(output_dir)
        if evaluation["returncode"] == 0:
            result["status"] = "scored"
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"{type(exc).__name__}: {exc}"

    result_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    try:
        results_volume.commit()
    except Exception as exc:  # noqa: BLE001
        result["volume_commit_error"] = f"{type(exc).__name__}: {exc}"
        result_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return json.dumps(result, indent=2, sort_keys=True)
