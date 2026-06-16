#!/usr/bin/env python3
"""Preflight the official BFCL candidate slice without running generation."""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.json"
DEFAULT_JSON_OUTPUT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-bfcl-preflight-20260616.json"
DEFAULT_MD_OUTPUT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-bfcl-preflight-20260616.md"
BFCL_BIN = Path("/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl")
EXPECTED_SUITE = "official-bfcl"
EXPECTED_RUN_ID = "qwen3-v4-peft-official-bfcl-20260616"


@dataclass(frozen=True)
class EndpointProbe:
    base_url: str
    status: str
    detail: str
    models: list[str]


def load_queue(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_bfcl_item(queue: dict[str, Any]) -> dict[str, Any]:
    for item in queue.get("items", []):
        if isinstance(item, dict) and item.get("suite") == EXPECTED_SUITE:
            return item
    raise ValueError(f"{EXPECTED_SUITE} not found in official candidate suite queue")


def command_version(command: Path) -> dict[str, Any]:
    if not command.exists():
        return {"path": str(command), "present": False, "executable": False, "version_output": ""}
    executable = os.access(command, os.X_OK)
    version_output = ""
    if executable:
        result = subprocess.run([str(command), "--help"], capture_output=True, text=True, timeout=20)
        for line in (result.stdout or result.stderr).splitlines():
            if line.strip():
                version_output = line.strip()
                break
    return {"path": str(command), "present": True, "executable": executable, "version_output": version_output}


def is_ssd_backed(path: str) -> bool:
    return path.startswith("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/")


def probe_endpoint(base_url: str, timeout_s: float) -> EndpointProbe:
    if not base_url:
        return EndpointProbe(base_url="", status="not-configured", detail="REMOTE_OPENAI_BASE_URL was not set.", models=[])
    url = base_url.rstrip("/") + "/models"
    request = Request(url, headers={"Authorization": f"Bearer {os.environ.get('REMOTE_OPENAI_API_KEY', 'EMPTY')}"})
    try:
        with urlopen(request, timeout=timeout_s) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (TimeoutError, URLError, socket.timeout, OSError, json.JSONDecodeError) as exc:
        return EndpointProbe(base_url=base_url, status="unreachable", detail=f"{type(exc).__name__}: {exc}", models=[])

    models: list[str] = []
    for item in payload.get("data", []):
        if isinstance(item, dict) and item.get("id"):
            models.append(str(item["id"]))
    return EndpointProbe(base_url=base_url, status="reachable", detail="GET /v1/models returned JSON.", models=models)


def build_report(
    queue_path: Path = DEFAULT_QUEUE,
    created_at: str | None = None,
    base_url: str | None = None,
    timeout_s: float = 5.0,
) -> dict[str, Any]:
    queue = load_queue(queue_path)
    item = find_bfcl_item(queue)
    bfcl = command_version(BFCL_BIN)
    endpoint = probe_endpoint(base_url if base_url is not None else os.environ.get("REMOTE_OPENAI_BASE_URL", ""), timeout_s)
    output_root = str(item.get("output_root", ""))
    command = str(item.get("local_command", ""))

    checks = {
        "queue_item_present": True,
        "suite_status_missing": item.get("status") == "missing",
        "run_id_matches": item.get("run_id") == EXPECTED_RUN_ID,
        "output_root_ssd_backed": is_ssd_backed(output_root),
        "local_command_uses_bfcl_generate": "bfcl generate" in command,
        "local_command_uses_bfcl_evaluate": "bfcl evaluate" in command,
        "bfcl_cli_executable": bool(bfcl["present"] and bfcl["executable"]),
        "endpoint_reachable": endpoint.status == "reachable",
    }
    blockers: list[str] = []
    for name, passed in checks.items():
        if not passed and name != "endpoint_reachable":
            blockers.append(name.replace("_", " "))
    if endpoint.status != "reachable":
        blockers.append("OpenAI-compatible endpoint is not reachable/configured")
    status = "ready-to-run" if not blockers else "blocked-endpoint-preflight"
    return {
        "created_at": created_at or datetime.now(UTC).isoformat(),
        "status": status,
        "suite": EXPECTED_SUITE,
        "run_id": EXPECTED_RUN_ID,
        "candidate": queue.get("candidate"),
        "base_model": queue.get("base_model"),
        "adapter": queue.get("adapter"),
        "queue_path": str(queue_path.relative_to(ROOT) if queue_path.is_relative_to(ROOT) else queue_path),
        "output_root": output_root,
        "bfcl_cli": bfcl,
        "endpoint": {
            "base_url": endpoint.base_url,
            "status": endpoint.status,
            "detail": endpoint.detail,
            "models": endpoint.models,
        },
        "checks": checks,
        "blockers": blockers,
        "local_command": command,
        "publication_boundary": item.get("publication_boundary", ""),
        "decision": (
            "Run official BFCL generate/evaluate only after endpoint_reachable is true; "
            "this preflight is not scored benchmark evidence."
        ),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 v4 Official BFCL Preflight",
        "",
        f"Date: {report['created_at']}",
        f"Status: `{report['status']}`",
        f"Suite: `{report['suite']}`",
        f"Run ID: `{report['run_id']}`",
        f"Candidate: `{report['candidate']}`",
        f"Adapter: `{report['adapter']}`",
        f"Output root: `{report['output_root']}`",
        "",
        "This report is a launch gate for the official BFCL slice. It does not contain BFCL scores.",
        "",
        "## Checks",
        "",
        "| Check | Pass |",
        "|---|---:|",
    ]
    for name, passed in report["checks"].items():
        lines.append(f"| `{name}` | `{str(passed).lower()}` |")
    lines.extend(
        [
            "",
            "## Endpoint",
            "",
            f"- Base URL: `{report['endpoint']['base_url'] or '(not configured)'}`",
            f"- Status: `{report['endpoint']['status']}`",
            f"- Detail: {report['endpoint']['detail']}",
            f"- Models: `{', '.join(report['endpoint']['models']) if report['endpoint']['models'] else '(none)'}`",
            "",
            "## BFCL CLI",
            "",
            f"- Path: `{report['bfcl_cli']['path']}`",
            f"- Present: `{str(report['bfcl_cli']['present']).lower()}`",
            f"- Executable: `{str(report['bfcl_cli']['executable']).lower()}`",
            f"- Help/version line: `{report['bfcl_cli']['version_output']}`",
            "",
            "## Blockers",
            "",
        ]
    )
    if report["blockers"]:
        for blocker in report["blockers"]:
            lines.append(f"- {blocker}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Command",
            "",
            "```bash",
            report["local_command"],
            "```",
            "",
            "## Decision",
            "",
            report["decision"],
            f"Publication boundary: {report['publication_boundary']}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_MD_OUTPUT)
    parser.add_argument("--base-url", default=None, help="Override REMOTE_OPENAI_BASE_URL for endpoint probing.")
    parser.add_argument("--timeout-s", type=float, default=5.0)
    parser.add_argument("--created-at", help="Override timestamp for deterministic regeneration checks.")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    report = build_report(
        queue_path=args.queue,
        created_at=args.created_at,
        base_url=args.base_url,
        timeout_s=args.timeout_s,
    )
    if not args.no_write:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        args.output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"status": report["status"], "blockers": report["blockers"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
