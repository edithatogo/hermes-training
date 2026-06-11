#!/usr/bin/env python3
"""Bootstrap and smoke-test benchmark packages inside a Colab runtime.

The script is intentionally small: it proves that a Colab accelerator runtime
can host the official benchmark environment shape, but it does not download
benchmark datasets or run model inference.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.metadata as metadata
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


INSTALL_PROFILES: dict[str, tuple[str, ...]] = {
    "none": (),
    "general-core": (
        "jedi",
        "lm_eval",
        "evaluate",
        "evalplus",
        "human-eval",
        "mteb",
        "sentence-transformers",
        "langdetect",
        "immutabledict",
        "tree-sitter",
    ),
    "bfcl-core": (
        "jedi",
        "bfcl-eval",
        "soundfile",
        "tree-sitter",
        "numpy",
        "torch",
        "transformers",
        "sentence-transformers",
    ),
}

SMOKE_MODES = {
    "general": {
        "imports": (
            "lm_eval",
            "langdetect",
            "immutabledict",
            "evaluate",
            "evalplus",
            "human_eval",
            "mteb",
            "sentence_transformers",
            "transformers",
            "torch",
        ),
        "distributions": (
            "lm_eval",
            "langdetect",
            "immutabledict",
            "evaluate",
            "evalplus",
            "human-eval",
            "mteb",
            "torch",
            "transformers",
            "sentence-transformers",
            "tree-sitter",
        ),
        "cli": (("lm_eval", "--help"),),
    },
    "bfcl": {
        "imports": (
            "bfcl_eval",
            "soundfile",
            "tree_sitter",
            "numpy",
            "torch",
            "transformers",
            "sentence_transformers",
        ),
        "distributions": (
            "bfcl-eval",
            "soundfile",
            "tree-sitter",
            "numpy",
            "torch",
            "transformers",
            "sentence-transformers",
        ),
        "cli": (("bfcl", "--help"),),
    },
}


def run_command(command: list[str], timeout_s: int) -> dict[str, Any]:
    result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=timeout_s)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def check_imports(names: tuple[str, ...]) -> dict[str, str]:
    results: dict[str, str] = {}
    for name in names:
        try:
            importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001
            results[name] = f"fail: {type(exc).__name__}: {exc}"
        else:
            results[name] = "ok"
    return results


def package_versions(names: tuple[str, ...]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in names:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "missing"
    return versions


def run_cli(command: tuple[str, ...]) -> dict[str, Any]:
    env = os.environ.copy()
    env["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{env.get('PATH', '')}"
    resolved = list(command)
    executable = Path(sys.executable).parent / command[0]
    if executable.exists():
        resolved[0] = str(executable)
    return run_command(resolved, timeout_s=30)


def smoke(mode: str) -> dict[str, Any]:
    cfg = SMOKE_MODES[mode]
    pip_check = run_command([sys.executable, "-m", "pip", "check"], timeout_s=60)
    cli_results = [run_cli(command) for command in cfg["cli"]]
    result = {
        "mode": mode,
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "imports": check_imports(cfg["imports"]),
        "versions": package_versions(cfg["distributions"]),
        "pip_check": pip_check,
        "cli": cli_results,
    }
    result["ok"] = all(value == "ok" for value in result["imports"].values())
    result["ok"] = result["ok"] and all(value != "missing" for value in result["versions"].values())
    result["ok"] = result["ok"] and pip_check["returncode"] == 0
    result["ok"] = result["ok"] and all(item["returncode"] == 0 for item in cli_results)
    return result


def install_profile(profile: str, timeout_s: int) -> dict[str, Any]:
    packages = INSTALL_PROFILES[profile]
    if not packages:
        return {"profile": profile, "packages": [], "returncode": 0, "skipped": True}
    command = [sys.executable, "-m", "pip", "install", "--quiet", *packages]
    result = run_command(command, timeout_s=timeout_s)
    result["profile"] = profile
    result["packages"] = list(packages)
    return result


def runtime_details() -> dict[str, Any]:
    details: dict[str, Any] = {
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "created_at": datetime.now(UTC).isoformat(),
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("general", "bfcl"), default="general")
    parser.add_argument("--install-profile", choices=sorted(INSTALL_PROFILES), default="general-core")
    parser.add_argument("--install-timeout", type=int, default=900)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    install = install_profile(args.install_profile, timeout_s=args.install_timeout)
    result: dict[str, Any] = {
        "status": "blocked",
        "mode": args.mode,
        "install": install,
        "runtime": runtime_details(),
        "claim_boundary": "Environment smoke only; no benchmark score, dataset download, or model inference.",
    }
    if install.get("returncode") == 0:
        smoke_result = smoke(args.mode)
        result["smoke"] = smoke_result
        result["status"] = "scored" if smoke_result["ok"] else "blocked"

    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["status"] == "scored" else 1


if __name__ == "__main__":
    raise SystemExit(main())
