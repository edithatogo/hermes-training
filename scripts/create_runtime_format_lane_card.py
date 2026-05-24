#!/usr/bin/env python3
"""Create an SSD-backed proof card for a runtime/training format lane."""
from __future__ import annotations

import argparse
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
LANES_PATH = ROOT / "RUNTIME_FORMAT_LANES.yaml"
DEFAULT_OUTPUT_ROOT = Path("/Volumes/PortableSSD/hermes-evals/runtime-format-lanes")


def slug(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    return normalized or "unnamed"


def load_lanes(path: Path = LANES_PATH) -> dict[str, dict[str, Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("lanes"), list):
        raise ValueError(f"{path}: expected lanes list")
    lanes: dict[str, dict[str, Any]] = {}
    for item in data["lanes"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError(f"{path}: invalid lane entry")
        lanes[item["id"]] = item
    return lanes


def bullet_list(values: list[str], indent: str = "  ") -> str:
    return "\n".join(f"{indent}- {value}" for value in values)


def render_card(
    lane: dict[str, Any],
    model: str,
    run_name: str,
    command: str,
    artifact_path: str,
    endpoint: str,
    operator: str,
    date: str,
    output_root: Path,
) -> str:
    tools = ", ".join(lane.get("tools", []))
    artifact_formats = ", ".join(lane.get("artifact_formats", []))
    command_block = command.strip() or "# command goes here"
    endpoint_line = f"- Endpoint: `{endpoint}`" if endpoint else "- Endpoint:"
    artifact_line = f"- Artifact path: `{artifact_path}`" if artifact_path else "- Artifact path:"
    lines = [
        "# Runtime Format Lane Proof Card",
        "",
        "## Identity",
        "",
        f"- Run name: {run_name}",
        f"- Date: {date}",
        f"- Operator: {operator}",
        f"- Format lane: `{lane['id']}`",
        f"- Platform lane: `{lane['primary_environment']}`",
        f"- Candidate model: `{model}`",
        "- Model revision:",
        f"- Runtime/tool: {tools}",
        artifact_line,
        endpoint_line,
        f"- Output root: `{output_root}`",
        "",
        "## Lane Contract",
        "",
        f"- Lane kind: `{lane['kind']}`",
        f"- Primary environment: `{lane['primary_environment']}`",
        f"- Tools: {tools}",
        f"- Artifact formats: {artifact_formats}",
        "- Proof required:",
        bullet_list(lane.get("proof_required", [])),
        "- Not for:",
        bullet_list(lane.get("not_for", [])),
        "",
        "## Command",
        "",
        "```bash",
        "source scripts/env.sh",
        command_block,
        "```",
        "",
        "## Proof Checklist",
        "",
        "- [ ] Source, license, model ID, and revision recorded.",
        "- [ ] Large artifacts and outputs are under `/Volumes/PortableSSD`.",
        "- [ ] Runtime or training command is reproducible.",
        "- [ ] Endpoint contract or native invocation contract is documented.",
        "- [ ] Smoke prompt or task-specific smoke passed.",
        "- [ ] Hermes integration boundary is clear.",
        "- [ ] Benchmark boundary is clear: runtime proof, teacher evidence, or publishable benchmark.",
        "",
        "## Results",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Status | pending |",
        "| Latency | |",
        "| Peak memory | |",
        "| Benchmark output | |",
        "| Failure mode | |",
        "| Decision | |",
        "",
        "## Notes",
        "",
        "- Generated from `RUNTIME_FORMAT_LANES.yaml`; fill results only after the run completes.",
        "",
    ]
    return "\n".join(lines)


def default_output_path(lane_id: str, model: str, run_name: str) -> Path:
    return DEFAULT_OUTPUT_ROOT / slug(lane_id) / slug(model) / f"{slug(run_name)}.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--run-name")
    parser.add_argument("--command", default="")
    parser.add_argument("--artifact-path", default="")
    parser.add_argument("--endpoint", default="")
    parser.add_argument("--operator", default="codex")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--print", action="store_true", dest="print_only")
    args = parser.parse_args()

    lanes = load_lanes()
    if args.lane_id not in lanes:
        available = ", ".join(sorted(lanes))
        raise SystemExit(f"unknown lane {args.lane_id!r}; available lanes: {available}")

    date = datetime.now(UTC).strftime("%Y-%m-%d")
    run_name = args.run_name or f"{slug(args.model)}-{args.lane_id}-{date.replace('-', '')}"
    output = args.output or default_output_path(args.lane_id, args.model, run_name)
    card = render_card(
        lanes[args.lane_id],
        args.model,
        run_name,
        args.command,
        args.artifact_path,
        args.endpoint,
        args.operator,
        date,
        output.parent,
    )

    if args.print_only:
        print(card, end="")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(card, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
