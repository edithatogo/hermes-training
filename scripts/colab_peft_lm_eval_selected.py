#!/usr/bin/env python3
"""Run a bounded lm-eval selected-task pilot for a PEFT adapter inside Colab."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tarfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable


CONFIG_PATH = Path(os.environ.get("LM_EVAL_CONFIG_JSON", "/content/qwen3-v4-peft-lm-eval-config.json"))
DEFAULT_TASKS = "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande"


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    with CONFIG_PATH.open(encoding="utf-8") as handle:
        config = json.load(handle)
    if not isinstance(config, dict):
        raise TypeError(f"{CONFIG_PATH} must contain a JSON object")
    return config


CONFIG = load_config()


def setting(name: str, env_name: str, default: Any) -> Any:
    if env_name in os.environ:
        return os.environ[env_name]
    return CONFIG.get(name, default)


def parse_optional_text(value: Any) -> str | None:
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


def parse_extra_model_args(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, list):
        return tuple(str(item) for item in value if str(item))
    return tuple(arg for arg in str(value).split(",") if arg)


ADAPTER_TARBALL_TEXT = parse_optional_text(
    setting("adapter_tarball", "PEFT_ADAPTER_TARBALL", "/content/qwen3-v4-peft-conversion-20260613.tar.gz")
)
ADAPTER_TARBALL = Path(ADAPTER_TARBALL_TEXT) if ADAPTER_TARBALL_TEXT is not None else None
ADAPTER_DIR = Path(setting("adapter_dir", "PEFT_ADAPTER_DIR", "/content/qwen3-v4-peft-conversion-20260613"))
BASE_MODEL = str(setting("base_model", "PEFT_BASE_MODEL", "Qwen/Qwen3-4B"))
TASKS = str(setting("tasks", "LM_EVAL_TASKS", DEFAULT_TASKS))
LIMIT = parse_optional_text(setting("limit", "LM_EVAL_LIMIT", "5"))
BATCH_SIZE = str(setting("batch_size", "LM_EVAL_BATCH_SIZE", "1"))
DTYPE = str(setting("dtype", "LM_EVAL_DTYPE", "float16"))
USE_4BIT = parse_bool(setting("use_4bit", "LM_EVAL_USE_4BIT", True))
TIMEOUT_S = int(setting("timeout_s", "LM_EVAL_TIMEOUT_S", "3600"))
TRANSFORMERS_SPEC = str(setting("transformers_spec", "LM_EVAL_TRANSFORMERS_SPEC", "transformers>=4.56,<5"))
EXTRA_MODEL_ARGS = parse_extra_model_args(setting("extra_model_args", "LM_EVAL_EXTRA_MODEL_ARGS", None))
OUTPUT_DIR = Path(setting("output_dir", "LM_EVAL_OUTPUT_DIR", "/content/qwen3-v4-peft-lm-eval-selected-limit5"))
OUTPUT_JSON = Path(setting("result_json", "LM_EVAL_RESULT_JSON", "/content/qwen3-v4-peft-lm-eval-selected-limit5.json"))
RUN_ID = str(setting("run_id", "RUN_ID", OUTPUT_JSON.stem))
HF_RESULTS_REPO = parse_optional_text(setting("hf_results_repo", "HF_RESULTS_REPO", None))
UPLOAD_CHECKPOINTS = parse_bool(setting("upload_checkpoints", "LM_EVAL_UPLOAD_CHECKPOINTS", False))
EVAL_CHECKPOINT_INTERVAL_S = int(setting("eval_checkpoint_interval_s", "LM_EVAL_CHECKPOINT_INTERVAL_S", "300"))


def run_command(
    command: list[str],
    timeout_s: int,
    *,
    heartbeat_interval_s: int | None = None,
    heartbeat: Callable[[float], None] | None = None,
) -> dict[str, Any]:
    started = time.time()
    if heartbeat is None or heartbeat_interval_s is None or heartbeat_interval_s <= 0:
        try:
            result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=timeout_s)
        except subprocess.TimeoutExpired as exc:
            return {
                "command": command,
                "returncode": None,
                "timed_out": True,
                "duration_s": time.time() - started,
                "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
                "stderr_tail": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
            }
        return {
            "command": command,
            "returncode": result.returncode,
            "timed_out": False,
            "duration_s": time.time() - started,
            "stdout_tail": result.stdout[-4000:],
            "stderr_tail": result.stderr[-4000:],
        }

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)  # noqa: S603
    try:
        while True:
            elapsed = time.time() - started
            remaining = timeout_s - elapsed
            if remaining <= 0:
                process.kill()
                stdout, stderr = process.communicate()
                return {
                    "command": command,
                    "returncode": None,
                    "timed_out": True,
                    "duration_s": time.time() - started,
                    "stdout_tail": stdout[-4000:],
                    "stderr_tail": stderr[-4000:],
                }
            wait_s = min(float(heartbeat_interval_s), remaining)
            try:
                stdout, stderr = process.communicate(timeout=wait_s)
                return {
                    "command": command,
                    "returncode": process.returncode,
                    "timed_out": False,
                    "duration_s": time.time() - started,
                    "stdout_tail": stdout[-4000:],
                    "stderr_tail": stderr[-4000:],
                }
            except subprocess.TimeoutExpired:
                heartbeat(time.time() - started)
    except Exception:
        process.kill()
        process.communicate()
        raise


def summarize_command_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "returncode": result.get("returncode"),
        "timed_out": result.get("timed_out"),
        "duration_s": result.get("duration_s"),
    }


def runtime_details() -> dict[str, Any]:
    details: dict[str, Any] = {
        "created_at": datetime.now(UTC).isoformat(),
        "python": sys.version.split()[0],
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


def extract_adapter() -> None:
    if ADAPTER_TARBALL is None:
        if not ADAPTER_DIR.exists():
            raise FileNotFoundError(f"adapter_dir does not exist and adapter_tarball is null: {ADAPTER_DIR}")
        return
    if not ADAPTER_TARBALL.exists():
        raise FileNotFoundError(ADAPTER_TARBALL)
    ADAPTER_DIR.parent.mkdir(parents=True, exist_ok=True)
    root = ADAPTER_DIR.parent.resolve()
    with tarfile.open(ADAPTER_TARBALL, "r:gz") as archive:
        for member in archive.getmembers():
            target = (ADAPTER_DIR.parent / member.name).resolve()
            if not target.is_relative_to(root):
                raise ValueError(f"Unsafe tar member path: {member.name}")
        archive.extractall(ADAPTER_DIR.parent)


def collect_result_files() -> list[str]:
    if not OUTPUT_DIR.exists():
        return []
    return sorted(str(path.relative_to(OUTPUT_DIR)) for path in OUTPUT_DIR.rglob("*") if path.is_file())


def write_checkpoint(result: dict[str, Any], phase: str) -> None:
    result["checkpoint_phase"] = phase
    result["checkpoint_at"] = datetime.now(UTC).isoformat()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("COLAB_LM_EVAL_CHECKPOINT " + json.dumps({"phase": phase, "status": result.get("status"), "path": str(OUTPUT_JSON)}, sort_keys=True), flush=True)
    if UPLOAD_CHECKPOINTS:
        result["checkpoint_upload"] = upload_results(OUTPUT_JSON, OUTPUT_DIR, RUN_ID, phase)
        OUTPUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("COLAB_LM_EVAL_CHECKPOINT_UPLOAD " + json.dumps(result["checkpoint_upload"], sort_keys=True), flush=True)


def upload_results(result_json: Path, output_dir: Path, run_id: str, phase: str = "final") -> dict[str, Any]:
    if not HF_RESULTS_REPO:
        return {"status": "skipped", "reason": "HF_RESULTS_REPO not set"}
    token = os.environ.get("HF_TOKEN")
    if not token:
        return {"status": "blocked", "repo_id": HF_RESULTS_REPO, "reason": "HF_TOKEN not set"}
    try:
        from huggingface_hub import HfApi

        api = HfApi(token=token)
        api.create_repo(HF_RESULTS_REPO, repo_type="dataset", exist_ok=True, private=False)
        uploaded: list[str] = []
        if result_json.exists():
            api.upload_file(
                repo_id=HF_RESULTS_REPO,
                repo_type="dataset",
                path_or_fileobj=str(result_json),
                path_in_repo=f"{run_id}/{phase}/summary.json",
                commit_message=f"Upload {run_id} {phase} summary",
            )
            uploaded.append(f"{run_id}/{phase}/summary.json")
        if phase == "final" and output_dir.exists():
            api.upload_folder(
                repo_id=HF_RESULTS_REPO,
                repo_type="dataset",
                folder_path=str(output_dir),
                path_in_repo=f"{run_id}/lm-eval-output",
                commit_message=f"Upload {run_id} lm-eval output",
            )
            uploaded.append(f"{run_id}/lm-eval-output")
        return {"status": "uploaded", "repo_id": HF_RESULTS_REPO, "paths": uploaded}
    except Exception as exc:  # noqa: BLE001
        return {"status": "blocked", "repo_id": HF_RESULTS_REPO, "error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    accelerate_install = run_command(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--quiet",
            "--upgrade",
            "--no-deps",
            "accelerate",
        ],
        timeout_s=600,
    )
    install = run_command(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--quiet",
            "--upgrade",
            "lm_eval[hf]",
            TRANSFORMERS_SPEC,
            "peft",
            "bitsandbytes",
            "safetensors",
        ],
        timeout_s=900,
    )
    result: dict[str, Any] = {
        "status": "blocked",
        "probe": "colab-peft-lm-eval-selected",
        "claim_boundary": "Bounded selected-task pilot only; not a full candidate scorecard.",
        "run_id": RUN_ID,
        "adapter_tarball": str(ADAPTER_TARBALL) if ADAPTER_TARBALL is not None else None,
        "adapter_dir": str(ADAPTER_DIR),
        "base_model": BASE_MODEL,
        "config_path": str(CONFIG_PATH) if CONFIG_PATH.exists() else None,
        "tasks": TASKS,
        "limit": LIMIT,
        "batch_size": BATCH_SIZE,
        "dtype": DTYPE,
        "use_4bit": USE_4BIT,
        "timeout_s": TIMEOUT_S,
        "eval_checkpoint_interval_s": EVAL_CHECKPOINT_INTERVAL_S,
        "transformers_spec": TRANSFORMERS_SPEC,
        "extra_model_args": EXTRA_MODEL_ARGS,
        "output_dir": str(OUTPUT_DIR),
        "result_json": str(OUTPUT_JSON),
        "hf_results_repo": HF_RESULTS_REPO,
        "upload_checkpoints": UPLOAD_CHECKPOINTS,
        "accelerate_install": accelerate_install,
        "install": install,
        "runtime": runtime_details(),
    }
    write_checkpoint(result, "dependencies-installed")
    try:
        if accelerate_install["returncode"] != 0:
            raise RuntimeError("accelerate install failed")
        if install["returncode"] != 0:
            raise RuntimeError("dependency install failed")
        extract_adapter()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        write_checkpoint(result, "adapter-ready")
        model_arg_parts = [
            f"pretrained={BASE_MODEL}",
            f"peft={ADAPTER_DIR}",
            "device_map=auto",
            f"dtype={DTYPE}",
            "trust_remote_code=True",
        ]
        if USE_4BIT:
            model_arg_parts.extend(["load_in_4bit=True", f"bnb_4bit_compute_dtype={DTYPE}"])
        model_args = ",".join([*model_arg_parts, *EXTRA_MODEL_ARGS])
        command = [
            sys.executable,
            "-m",
            "lm_eval",
            "--model",
            "hf",
            "--model_args",
            model_args,
            "--tasks",
            TASKS,
            "--batch_size",
            BATCH_SIZE,
            "--output_path",
            str(OUTPUT_DIR),
        ]
        if LIMIT is not None:
            command[command.index("--batch_size"):command.index("--batch_size")] = ["--limit", LIMIT]
        result["status"] = "running"
        result["evaluation_command"] = command
        write_checkpoint(result, "evaluation-running")

        def evaluation_heartbeat(elapsed_s: float) -> None:
            result["evaluation_elapsed_s"] = elapsed_s
            write_checkpoint(result, "evaluation-running")

        evaluation = run_command(
            command,
            timeout_s=TIMEOUT_S,
            heartbeat_interval_s=EVAL_CHECKPOINT_INTERVAL_S,
            heartbeat=evaluation_heartbeat,
        )
        result["evaluation"] = evaluation
        result.pop("evaluation_command", None)
        result["evaluation_summary"] = summarize_command_result(evaluation)
        result["result_files"] = collect_result_files()
        if evaluation["returncode"] == 0:
            result["status"] = "scored"
        else:
            result["status"] = "blocked"
        write_checkpoint(result, "evaluation-complete")
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["upload"] = upload_results(OUTPUT_JSON, OUTPUT_DIR, RUN_ID)
    OUTPUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
