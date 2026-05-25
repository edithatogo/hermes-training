"""User plugin that exposes the hermes-training mem0 read wrapper to Hermes."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    configured = os.environ.get("HERMES_TRAINING_ROOT")
    if configured:
        return Path(configured)
    return Path("/Volumes/PortableSSD/GitHub/hermes-training")


def _manifest_path() -> Path:
    return _repo_root() / "mem0" / "integration" / "hermes_agent_mem0_read_tool.json"


def _load_manifest() -> dict[str, Any]:
    return json.loads(_manifest_path().read_text(encoding="utf-8"))


def _check_available() -> tuple[bool, str]:
    try:
        manifest = _load_manifest()
    except Exception as exc:
        return False, f"Cannot read {_manifest_path()}: {exc}"
    command = manifest.get("command") or []
    missing = [part for part in command[:2] if not Path(part).exists()]
    if missing:
        return False, f"Missing command path(s): {', '.join(missing)}"
    return True, "hermes_mem0_read wrapper is available"


def _handle_mem0_read(**kwargs: Any) -> dict[str, Any]:
    manifest = _load_manifest()
    command = manifest["command"]
    try:
        completed = subprocess.run(
            command,
            input=json.dumps(kwargs),
            text=True,
            capture_output=True,
            timeout=90,
            check=False,
        )
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

    output = completed.stdout.strip()
    if completed.returncode != 0:
        return {
            "ok": False,
            "returncode": completed.returncode,
            "stdout": output,
            "stderr": completed.stderr.strip(),
        }
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {"ok": False, "error": "Wrapper did not return JSON", "stdout": output}


def register(ctx: Any) -> None:
    manifest = _load_manifest()
    ctx.register_tool(
        name=manifest["name"],
        toolset="hermes_mem0",
        schema=manifest["input_schema"],
        handler=_handle_mem0_read,
        check_fn=_check_available,
        description=manifest.get("description", ""),
    )
