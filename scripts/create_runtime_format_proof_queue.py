#!/usr/bin/env python3
"""Generate SSD-backed proof cards from RUNTIME_FORMAT_PROOF_QUEUE.yaml."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.create_runtime_format_lane_card import default_output_path, load_lanes, render_card  # noqa: E402

QUEUE_PATH = ROOT / "RUNTIME_FORMAT_PROOF_QUEUE.yaml"

REQUIRED_FIELDS = (
    "id",
    "lane_id",
    "model",
    "run_name",
    "status",
    "endpoint",
    "artifact_path",
    "command",
    "blocker",
)


def load_queue(path: Path = QUEUE_PATH) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    proofs = data.get("proofs")
    if not isinstance(proofs, list) or not proofs:
        raise ValueError(f"{path}: expected non-empty proofs list")
    return data


def validate_queue(queue: dict[str, Any], lane_ids: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for index, proof in enumerate(queue.get("proofs", []), 1):
        if not isinstance(proof, dict):
            errors.append(f"proofs[{index}]: expected mapping")
            continue
        proof_id = str(proof.get("id", f"<proof {index}>"))
        if proof_id in seen:
            errors.append(f"{proof_id}: duplicate proof id")
        seen.add(proof_id)
        for field in REQUIRED_FIELDS:
            if field not in proof:
                errors.append(f"{proof_id}: missing {field}")
        lane_id = proof.get("lane_id")
        if lane_id not in lane_ids:
            errors.append(f"{proof_id}: unknown lane_id {lane_id!r}")
        for field in ("id", "lane_id", "model", "run_name", "status", "command", "blocker"):
            value = proof.get(field)
            if not isinstance(value, str) or not value:
                errors.append(f"{proof_id}: {field} must be a non-empty string")
        for field in ("endpoint", "artifact_path"):
            if not isinstance(proof.get(field, ""), str):
                errors.append(f"{proof_id}: {field} must be a string")
    return errors


def render_queue_card(lane: dict[str, Any], proof: dict[str, Any], output: Path) -> str:
    card = render_card(
        lane,
        proof["model"],
        proof["run_name"],
        proof["command"],
        proof.get("artifact_path", ""),
        proof.get("endpoint", ""),
        "codex",
        "2026-05-24",
        output.parent,
    )
    return card + "\n## Queue State\n\n" + "\n".join(
        [
            f"- Proof ID: `{proof['id']}`",
            f"- Status: `{proof['status']}`",
            f"- Blocker: {proof['blocker']}",
            "",
        ]
    )


def output_path_for(proof: dict[str, Any], output_root: Path) -> Path:
    return output_root / proof["lane_id"] / proof["id"] / f"{proof['run_name']}.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=QUEUE_PATH)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--print", action="store_true", dest="print_only")
    args = parser.parse_args()

    lanes = load_lanes()
    queue = load_queue(args.queue)
    errors = validate_queue(queue, set(lanes))
    if errors:
        for error in errors:
            print(f"proof-queue: {error}")
        return 1

    output_root = args.output_root or Path(queue.get("output_root") or default_output_path("queue", "queue", "queue").parents[2])
    outputs: list[Path] = []
    for proof in queue["proofs"]:
        output = output_path_for(proof, output_root)
        outputs.append(output)
        if args.check:
            continue
        card = render_queue_card(lanes[proof["lane_id"]], proof, output)
        if args.print_only:
            print(f"--- {output}")
            print(card)
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(card, encoding="utf-8")

    if args.check:
        print(f"ok: {args.queue.name} ({len(outputs)} proofs)")
    elif not args.print_only:
        for output in outputs:
            print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
