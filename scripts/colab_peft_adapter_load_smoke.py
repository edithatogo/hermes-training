#!/usr/bin/env python3
"""Load-smoke a local PEFT adapter tarball inside Colab."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tarfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ADAPTER_TARBALL = Path(os.environ.get("PEFT_ADAPTER_TARBALL", "/content/qwen3-v4-peft-conversion-20260613.tar.gz"))
ADAPTER_DIR = Path(os.environ.get("PEFT_ADAPTER_DIR", "/content/qwen3-v4-peft-conversion-20260613"))
BASE_MODEL = os.environ.get("PEFT_BASE_MODEL", "Qwen/Qwen3-4B")
OUTPUT_JSON = Path(os.environ.get("PEFT_LOAD_SMOKE_JSON", "/content/qwen3-v4-peft-load-smoke.json"))


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
            "stdout_tail": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
        }
    return {
        "command": command,
        "returncode": result.returncode,
        "timed_out": False,
        "duration_s": time.time() - started,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
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
    if not ADAPTER_TARBALL.exists():
        raise FileNotFoundError(ADAPTER_TARBALL)
    ADAPTER_DIR.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(ADAPTER_TARBALL, "r:gz") as archive:
        for member in archive.getmembers():
            target = (ADAPTER_DIR.parent / member.name).resolve()
            if not target.is_relative_to(ADAPTER_DIR.parent.resolve()):
                raise ValueError(f"Unsafe tar member path: {member.name}")
        archive.extractall(ADAPTER_DIR.parent)


def smoke_load() -> dict[str, Any]:
    from peft import PeftConfig, PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    import torch

    peft_config = PeftConfig.from_pretrained(ADAPTER_DIR)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
    load_started = time.time()
    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        device_map="auto",
        quantization_config=quantization_config,
        trust_remote_code=True,
    )
    model = PeftModel.from_pretrained(base, ADAPTER_DIR)
    load_latency_s = time.time() - load_started
    prompt = "/no_think Return a JSON object with key ok and value true."
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    gen_started = time.time()
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=24, do_sample=False)
    generation_latency_s = time.time() - gen_started
    decoded = tokenizer.decode(output[0][inputs["input_ids"].shape[-1] :], skip_special_tokens=True)
    return {
        "peft_base_model": peft_config.base_model_name_or_path,
        "base_model": BASE_MODEL,
        "load_latency_s": load_latency_s,
        "generation_latency_s": generation_latency_s,
        "sample_output": decoded[:500],
    }


def main() -> int:
    install = run_command(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--quiet",
            "--upgrade",
            "transformers",
            "peft",
            "accelerate",
            "bitsandbytes",
            "safetensors",
        ],
        timeout_s=600,
    )
    result: dict[str, Any] = {
        "status": "blocked",
        "probe": "colab-peft-adapter-load-smoke",
        "claim_boundary": "Load smoke only; no benchmark score.",
        "adapter_tarball": str(ADAPTER_TARBALL),
        "adapter_dir": str(ADAPTER_DIR),
        "install": install,
        "runtime": runtime_details(),
    }
    try:
        if install["returncode"] != 0:
            raise RuntimeError("dependency install failed")
        extract_adapter()
        result["adapter_files"] = sorted(path.name for path in ADAPTER_DIR.iterdir() if path.is_file() and not path.name.startswith("._"))
        result["smoke"] = smoke_load()
        result["status"] = "loaded"
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"{type(exc).__name__}: {exc}"
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    OUTPUT_JSON.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
