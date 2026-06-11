#!/usr/bin/env python3
"""Read-only preflight for the Google Colab CLI lane."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def resolve_storage_root() -> Path:
    if os.environ.get("HERMES_STORAGE_ROOT"):
        return Path(os.environ["HERMES_STORAGE_ROOT"])
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD")
    return Path.cwd() / ".local-storage"


def run_version(command: str) -> dict[str, Any]:
    path = shutil.which(command)
    if not path:
        return {"installed": False, "path": "", "version": "", "error": f"{command} not found on PATH"}
    try:
        result = subprocess.run(
            [path, "version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except Exception as exc:  # noqa: BLE001
        return {"installed": True, "path": path, "version": "", "error": f"{type(exc).__name__}: {exc}"}
    output = (result.stdout or result.stderr).strip()
    return {
        "installed": True,
        "path": path,
        "version": output,
        "returncode": result.returncode,
        "error": "" if result.returncode == 0 else output,
    }


def build_report() -> dict[str, Any]:
    storage_root = resolve_storage_root()
    colab = run_version("colab")
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "status": "ready" if colab["installed"] and storage_root.exists() else "blocked",
        "colab": colab,
        "storage_root": str(storage_root),
        "storage_root_exists": storage_root.exists(),
        "recommended_install": "uv tool install google-colab-cli",
        "safe_smoke_commands": [
            "colab run --gpu T4 --timeout 120 scripts/colab_smoke.py",
            "colab run --tpu v5e1 --timeout 180 scripts/colab_smoke.py",
        ],
        "notes": [
            "This preflight is read-only and does not create a Colab runtime.",
            "Use google-colab-cli, not the older notebook-sync package named colab-cli.",
            "Download every run artifact back to the SSD before stopping the runtime.",
        ],
    }


def main() -> int:
    report = build_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
