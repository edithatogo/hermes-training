#!/usr/bin/env python3
"""Run Qwen3 v4 PEFT lm-eval selected tasks inside a Kaggle kernel."""
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
CONFIG_PATH = Path(os.environ.get("KAGGLE_SCORECARD_CONFIG", Path(__file__).with_name("kaggle-peft-lm-eval-config.json")))


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


def dependency_packages(use_4bit: bool) -> list[str]:
    packages = [
        "numpy<2",
        "lm_eval[hf]",
        "transformers==5.3.0",
        "peft",
        "safetensors",
        "accelerate",
        "huggingface_hub",
    ]
    if use_4bit:
        packages.append("bitsandbytes")
    return packages


def torch_compatibility_install(policy: str) -> list[str] | None:
    if policy in {"", "none", "None", "default"}:
        return None
    if policy == "p100-cu118":
        return [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--quiet",
            "--upgrade",
            "--index-url",
            "https://download.pytorch.org/whl/cu118",
            "torch==2.2.2",
            "torchvision==0.17.2",
            "torchaudio==2.2.2",
        ]
    raise ValueError(f"unsupported torch compatibility policy: {policy}")


def dependency_install_command(use_4bit: bool, torch_policy: str) -> list[str]:
    command = [sys.executable, "-m", "pip", "install", "--quiet"]
    if torch_policy in {"", "none", "None", "default"}:
        command.append("--upgrade")
    return [*command, *dependency_packages(use_4bit)]


def runtime_details() -> dict[str, Any]:
    details: dict[str, Any] = {"created_at": datetime.now(UTC).isoformat(), "python": sys.version.split()[0]}
    try:
        import torch

        details["torch"] = getattr(torch, "__version__", "unknown")
        details["cuda_available"] = bool(torch.cuda.is_available())
        details["cuda_device_name"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        details["cuda_device_capability"] = (
            ".".join(map(str, torch.cuda.get_device_capability(0))) if torch.cuda.is_available() else None
        )
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


def main() -> int:
    run_id = str(setting("run_id", "RUN_ID", f"qwen3-v4-peft-kaggle-lm-eval-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"))
    work_root = Path(setting("working_dir", "KAGGLE_WORKING_DIR", "/kaggle/working"))
    adapter_repo = str(setting("adapter_repo", "PEFT_ADAPTER_REPO", "edithatogo/qwen3-4b-hermes-lora-peft-converted"))
    adapter_dir = Path(setting("adapter_dir", "PEFT_ADAPTER_DIR", str(work_root / "qwen3-v4-peft-adapter")))
    base_model = str(setting("base_model", "PEFT_BASE_MODEL", "Qwen/Qwen3-4B"))
    tasks = str(setting("tasks", "LM_EVAL_TASKS", DEFAULT_TASKS))
    limit = optional_text(setting("limit", "LM_EVAL_LIMIT", None))
    batch_size = str(setting("batch_size", "LM_EVAL_BATCH_SIZE", "1"))
    dtype = str(setting("dtype", "LM_EVAL_DTYPE", "float16"))
    use_4bit = parse_bool(setting("use_4bit", "LM_EVAL_USE_4BIT", "0"))
    torch_policy = str(setting("torch_compatibility_policy", "KAGGLE_TORCH_COMPATIBILITY_POLICY", "p100-cu118"))
    timeout_s = int(setting("timeout_s", "LM_EVAL_TIMEOUT_S", "21600"))
    output_dir = Path(setting("output_dir", "LM_EVAL_OUTPUT_DIR", str(work_root / f"{run_id}-lm-eval-output")))
    result_json = Path(setting("result_json", "LM_EVAL_RESULT_JSON", str(work_root / f"{run_id}-summary.json")))

    install = run_command(dependency_install_command(use_4bit, torch_policy), timeout_s=1200)
    torch_install_command = torch_compatibility_install(torch_policy)
    # Kaggle's dependency solve can otherwise leave the final runtime on a
    # non-P100 torch build. Apply the compatibility policy last.
    torch_install = run_command(torch_install_command, timeout_s=1200) if torch_install_command else None
    result: dict[str, Any] = {
        "status": "blocked",
        "probe": "kaggle-peft-lm-eval-selected",
        "run_id": run_id,
        "claim_boundary": "No-limit benchmark claim only if every configured task completes without --limit.",
        "adapter_repo": adapter_repo,
        "adapter_dir": str(adapter_dir),
        "base_model": base_model,
        "config_path": str(CONFIG_PATH) if CONFIG_PATH.exists() else None,
        "tasks": tasks,
        "limit": limit,
        "batch_size": batch_size,
        "dtype": dtype,
        "use_4bit": use_4bit,
        "torch_compatibility_policy": torch_policy,
        "torch_install": torch_install,
        "output_dir": str(output_dir),
        "install": install,
        "runtime": runtime_details(),
    }

    try:
        if torch_install is not None and torch_install["returncode"] != 0:
            raise RuntimeError("torch compatibility install failed")
        if install["returncode"] != 0:
            raise RuntimeError("dependency install failed")
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
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
