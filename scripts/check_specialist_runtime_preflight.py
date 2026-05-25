#!/usr/bin/env python3
"""No-download preflight for specialist runtime lanes."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SSD_ROOT = Path(os.environ.get("HERMES_STORAGE_ROOT", "/Volumes/PortableSSD"))
DEFAULT_OUTPUT = ROOT / "reports" / "runtime" / "specialist-runtime-preflight-20260526.md"
DEFAULT_JSON_OUTPUT = ROOT / "reports" / "runtime" / "specialist-runtime-preflight-20260526.json"


@dataclass(frozen=True)
class Probe:
    lane_id: str
    model: str
    runtime: str
    commands: tuple[str, ...]
    modules: tuple[str, ...]
    artifact_paths: tuple[Path, ...]
    minimum_pass: str
    notes: str


PROBES = (
    Probe(
        lane_id="ktransformers-moe",
        model="Qwen/Qwen3.6-35B-A3B",
        runtime="KTransformers",
        commands=("ktransformers",),
        modules=("ktransformers",),
        artifact_paths=(
            SSD_ROOT / "huggingface" / "hub" / "models--Qwen--Qwen3.6-35B-A3B",
            SSD_ROOT / "models" / "Qwen" / "Qwen3.6-35B-A3B",
        ),
        minimum_pass="KTransformers import/CLI plus prepared Qwen3.6 weights.",
        notes="Do not treat the existing GGUF proof as KTransformers evidence; this lane needs native prepared weights and an invocation contract.",
    ),
    Probe(
        lane_id="liquid-leap-lfm",
        model="LiquidAI/LFM2-8B-A1B",
        runtime="LEAP/LFM specialist runtime",
        commands=("leap", "leap-finetune"),
        modules=("leap", "leap_finetune"),
        artifact_paths=(
            SSD_ROOT / "huggingface" / "hub" / "models--LiquidAI--LFM2-8B-A1B",
            SSD_ROOT / "huggingface" / "hub" / "models--LiquidAI--LFM2.5-1.2B-Instruct",
        ),
        minimum_pass="LEAP CLI/import plus a cached LFM family checkpoint or package.",
        notes="MLX and GGUF LFM proofs are separate; LEAP remains blocked until its own runtime/package path exists.",
    ),
    Probe(
        lane_id="recurrent-ssm-bitnet",
        model="RWKV/RWKV7-Goose-World3-2.9B-HF",
        runtime="RWKV native runtime",
        commands=("rwkv",),
        modules=("rwkv", "rwkvstic"),
        artifact_paths=(
            SSD_ROOT / "huggingface" / "hub" / "models--RWKV--RWKV7-Goose-World3-2.9B-HF",
            SSD_ROOT / "models" / "RWKV",
        ),
        minimum_pass="Native RWKV runtime plus exact cached checkpoint.",
        notes="Transformers compatibility alone is not enough for the recurrent runtime lane.",
    ),
    Probe(
        lane_id="recurrent-ssm-bitnet",
        model="microsoft/bitnet-b1.58-2B-4T",
        runtime="BitNet native runtime",
        commands=("bitnet", "bitnet-cli"),
        modules=("bitnet",),
        artifact_paths=(
            SSD_ROOT / "huggingface" / "hub" / "models--microsoft--bitnet-b1.58-2B-4T",
            SSD_ROOT / "GitHub" / "BitNet",
        ),
        minimum_pass="BitNet runtime plus exact cached checkpoint or local runtime checkout.",
        notes="Ternary/BitNet claims require the native runtime path, not generic transformer loading.",
    ),
    Probe(
        lane_id="recurrent-ssm-bitnet",
        model="state-spaces/mamba-family-watchlist",
        runtime="Mamba/SSM native runtime",
        commands=("mamba_ssm",),
        modules=("mamba_ssm",),
        artifact_paths=(
            SSD_ROOT / "huggingface" / "hub" / "models--state-spaces",
            SSD_ROOT / "models" / "mamba",
        ),
        minimum_pass="Mamba/SSM module plus exact checkpoint and invocation contract.",
        notes="Keep as architecture-family evidence until an exact public checkpoint and runtime are selected.",
    ),
)


def command_status(command: str) -> dict[str, Any]:
    path = shutil.which(command)
    return {"name": command, "present": bool(path), "path": path or ""}


def module_status(module: str) -> dict[str, Any]:
    try:
        spec = importlib.util.find_spec(module)
    except Exception:  # noqa: BLE001
        spec = None
    return {"name": module, "present": spec is not None}


def artifact_status(path: Path) -> dict[str, Any]:
    exists = path.exists()
    return {"path": str(path), "present": exists, "kind": "directory" if path.is_dir() else "file" if path.is_file() else "missing"}


def evaluate_probe(probe: Probe) -> dict[str, Any]:
    commands = [command_status(command) for command in probe.commands]
    modules = [module_status(module) for module in probe.modules]
    artifacts = [artifact_status(path) for path in probe.artifact_paths]
    runtime_present = any(item["present"] for item in commands) or any(item["present"] for item in modules)
    artifact_present = any(item["present"] for item in artifacts)
    status = "ready-for-smoke" if runtime_present and artifact_present else "blocked"
    blockers: list[str] = []
    if not runtime_present:
        blockers.append("runtime command/module not found")
    if not artifact_present:
        blockers.append("no matching SSD artifact path found")
    return {
        "lane_id": probe.lane_id,
        "model": probe.model,
        "runtime": probe.runtime,
        "status": status,
        "blockers": blockers,
        "commands": commands,
        "modules": modules,
        "artifacts": artifacts,
        "minimum_pass": probe.minimum_pass,
        "notes": probe.notes,
    }


def build_report() -> dict[str, Any]:
    items = [evaluate_probe(probe) for probe in PROBES]
    counts: dict[str, int] = {}
    for item in items:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "ssd_root": str(SSD_ROOT),
        "policy": "read-only; no installs, downloads, compute creation, or model conversion",
        "status": "passed" if items else "empty",
        "counts": counts,
        "items": items,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Specialist Runtime Preflight",
        "",
        f"Date: {report['created_at']}",
        f"SSD root: `{report['ssd_root']}`",
        f"Policy: {report['policy']}",
        "",
        "## Summary",
        "",
        "| Lane | Model | Runtime | Status | Blockers |",
        "|---|---|---|---|---|",
    ]
    for item in report["items"]:
        blockers = "; ".join(item["blockers"]) if item["blockers"] else "none"
        lines.append(f"| `{item['lane_id']}` | `{item['model']}` | {item['runtime']} | `{item['status']}` | {blockers} |")

    lines.extend(["", "## Details", ""])
    for item in report["items"]:
        lines.extend(
            [
                f"### {item['runtime']} / `{item['model']}`",
                "",
                f"- Minimum pass: {item['minimum_pass']}",
                f"- Notes: {item['notes']}",
                f"- Status: `{item['status']}`",
                "",
                "| Check | Name/path | Present |",
                "|---|---|---:|",
            ]
        )
        for command in item["commands"]:
            lines.append(f"| command | `{command['name']}` | `{str(command['present']).lower()}` |")
        for module in item["modules"]:
            lines.append(f"| python module | `{module['name']}` | `{str(module['present']).lower()}` |")
        for artifact in item["artifacts"]:
            lines.append(f"| artifact | `{artifact['path']}` | `{str(artifact['present']).lower()}` |")
        lines.append("")

    lines.extend(
        [
            "## Decision",
            "",
            "No specialist lane is promoted by this preflight. A lane can move to runtime smoke only after its native runtime and exact SSD artifact path are both present.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if not args.no_write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_markdown(report), encoding="utf-8")
        args.json_output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "counts")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
