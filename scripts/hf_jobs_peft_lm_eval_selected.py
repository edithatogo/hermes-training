#!/usr/bin/env python3
"""Run Qwen3 v4 PEFT lm-eval inside Hugging Face Jobs.

The job expects the converted PEFT adapter mounted at /adapter and optionally
uploads its JSON outputs to a Hub dataset for persistence.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


DEFAULT_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"


def optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    if text in {"", "none", "None", "null", "NULL"}:
        return None
    return text


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value) not in {"0", "false", "False", "no", "No"}


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


def resolve_adapter_dir(adapter_dir: Path) -> Path:
    if adapter_dir.exists():
        return adapter_dir
    repo_id = os.environ.get("PEFT_ADAPTER_REPO")
    if not repo_id and "/" in str(adapter_dir):
        repo_id = str(adapter_dir)
    if not repo_id:
        raise FileNotFoundError(f"adapter_dir not found: {adapter_dir}")
    from huggingface_hub import snapshot_download

    target = Path(os.environ.get("PEFT_ADAPTER_DOWNLOAD_DIR", "/tmp/qwen3-v4-peft-adapter"))
    snapshot_download(repo_id=repo_id, local_dir=target, local_dir_use_symlinks=False)
    return target


def upload_results(result_json: Path, output_dir: Path, run_id: str) -> dict[str, Any]:
    repo_id = os.environ.get("HF_RESULTS_REPO")
    if not repo_id:
        return {"status": "skipped", "reason": "HF_RESULTS_REPO not set"}
    token = os.environ.get("HF_TOKEN")
    if not token:
        return {"status": "blocked", "reason": "HF_TOKEN not set"}
    try:
        from huggingface_hub import HfApi

        api = HfApi(token=token)
        api.create_repo(repo_id, repo_type="dataset", exist_ok=True, private=False)
        uploaded: list[str] = []
        if result_json.exists():
            api.upload_file(
                repo_id=repo_id,
                repo_type="dataset",
                path_or_fileobj=str(result_json),
                path_in_repo=f"{run_id}/summary.json",
                commit_message=f"Upload {run_id} summary",
            )
            uploaded.append(f"{run_id}/summary.json")
        if output_dir.exists():
            api.upload_folder(
                repo_id=repo_id,
                repo_type="dataset",
                folder_path=str(output_dir),
                path_in_repo=f"{run_id}/lm-eval-output",
                commit_message=f"Upload {run_id} lm-eval output",
            )
            uploaded.append(f"{run_id}/lm-eval-output")
        return {"status": "uploaded", "repo_id": repo_id, "paths": uploaded}
    except Exception as exc:  # noqa: BLE001
        return {"status": "blocked", "repo_id": repo_id, "error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    run_id = os.environ.get("RUN_ID", f"qwen3-v4-peft-hf-jobs-lm-eval-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    adapter_dir = Path(os.environ.get("PEFT_ADAPTER_DIR", "/adapter"))
    base_model = os.environ.get("PEFT_BASE_MODEL", "Qwen/Qwen3-4B")
    tasks = os.environ.get("LM_EVAL_TASKS", DEFAULT_TASKS)
    limit = optional_text(os.environ.get("LM_EVAL_LIMIT"))
    batch_size = os.environ.get("LM_EVAL_BATCH_SIZE", "1")
    dtype = os.environ.get("LM_EVAL_DTYPE", "float16")
    use_4bit = parse_bool(os.environ.get("LM_EVAL_USE_4BIT", "1"))
    timeout_s = int(os.environ.get("LM_EVAL_TIMEOUT_S", "21600"))
    output_dir = Path(os.environ.get("LM_EVAL_OUTPUT_DIR", f"/tmp/{run_id}/lm-eval-output"))
    result_json = Path(os.environ.get("LM_EVAL_RESULT_JSON", f"/tmp/{run_id}/summary.json"))

    result: dict[str, Any] = {
        "status": "blocked",
        "probe": "hf-jobs-peft-lm-eval-selected",
        "run_id": run_id,
        "claim_boundary": "No-limit benchmark claim only if every configured task completes without --limit.",
        "adapter_dir": str(adapter_dir),
        "base_model": base_model,
        "tasks": tasks,
        "limit": limit,
        "batch_size": batch_size,
        "dtype": dtype,
        "use_4bit": use_4bit,
        "output_dir": str(output_dir),
        "runtime": runtime_details(),
    }

    try:
        adapter_dir = resolve_adapter_dir(adapter_dir)
        result["adapter_dir"] = str(adapter_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        result_json.parent.mkdir(parents=True, exist_ok=True)
        model_arg_parts = [
            f"pretrained={base_model}",
            f"peft={adapter_dir}",
            "device_map=auto",
            f"dtype={dtype}",
            "trust_remote_code=True",
        ]
        if use_4bit:
            model_arg_parts.extend(["load_in_4bit=True", f"bnb_4bit_compute_dtype={dtype}"])
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
    result["upload"] = upload_results(result_json, output_dir, run_id)
    result_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
