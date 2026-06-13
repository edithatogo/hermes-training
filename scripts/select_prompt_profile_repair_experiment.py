#!/usr/bin/env python3
"""Select or explicitly run one prompt/profile repair experiment."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERIMENTS = ROOT / "reports/benchmark/coverage/prompt-profile-repair-experiments-20260614.json"
DEFAULT_SELECTION_JSON = ROOT / "reports/benchmark/coverage/prompt-profile-repair-selection-20260614.json"
DEFAULT_SELECTION_MD = ROOT / "reports/benchmark/coverage/prompt-profile-repair-selection-20260614.md"
ENDPOINT_PLACEHOLDER = "http://127.0.0.1:<port>/v1"


def load_experiments(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    experiments = data.get("experiments", [])
    if not isinstance(experiments, list):
        raise ValueError(f"{path}: experiments must be a list")
    return [item for item in experiments if isinstance(item, dict)]


def select_experiment(
    experiments: list[dict[str, Any]],
    candidate: str | None,
    variant: str | None,
    index: int | None,
) -> dict[str, Any]:
    if index is not None:
        if index < 1 or index > len(experiments):
            raise ValueError(f"--index must be between 1 and {len(experiments)}")
        return experiments[index - 1]
    if not candidate or not variant:
        raise ValueError("provide either --index or both --candidate and --variant")
    matches = [
        item
        for item in experiments
        if item.get("candidate") == candidate and item.get("variant") == variant
    ]
    if not matches:
        raise ValueError(f"no experiment found for candidate={candidate!r} variant={variant!r}")
    if len(matches) > 1:
        raise ValueError(f"ambiguous experiment for candidate={candidate!r} variant={variant!r}")
    return matches[0]


def command_with_overrides(command: str, base_url: str | None = None) -> str:
    if base_url:
        return command.replace(ENDPOINT_PLACEHOLDER, base_url)
    return command


def build_selection(
    experiment: dict[str, Any],
    command: str,
    execute: bool,
    confirm_local_run: bool,
) -> dict[str, Any]:
    blockers: list[str] = []
    if execute and not confirm_local_run:
        blockers.append("--confirm-local-run is required with --execute")
    if execute and ENDPOINT_PLACEHOLDER in command:
        blockers.append("--base-url is required for endpoint experiments before --execute")
    status = "ready-to-run" if execute and not blockers else "dry-run"
    if blockers:
        status = "blocked"
    return {
        "status": status,
        "execute": execute,
        "confirm_local_run": confirm_local_run,
        "candidate": experiment.get("candidate"),
        "variant": experiment.get("variant"),
        "runner": experiment.get("runner"),
        "raw_output_promotion_allowed": experiment.get("raw_output_promotion_allowed"),
        "goal": experiment.get("goal"),
        "promotion_boundary": experiment.get("promotion_boundary"),
        "command": command,
        "blockers": blockers,
        "claim_boundary": "A selected repair run is not promotion evidence until raw strict outputs and downstream held-out, pilot, official benchmark, latency, and rollback gates pass.",
    }


def render_markdown(selection: dict[str, Any]) -> str:
    lines = [
        "# Prompt/Profile Repair Selection",
        "",
        f"- Status: `{selection['status']}`",
        f"- Candidate: `{selection['candidate']}`",
        f"- Variant: `{selection['variant']}`",
        f"- Runner: `{selection['runner']}`",
        f"- Raw-output promotion allowed: `{selection['raw_output_promotion_allowed']}`",
        f"- Goal: {selection['goal']}",
        f"- Boundary: {selection['claim_boundary']}",
        "",
        "## Command",
        "",
        "```bash",
        str(selection["command"]),
        "```",
        "",
    ]
    if selection["blockers"]:
        lines.extend(["## Blockers", ""])
        lines.extend(f"- {blocker}" for blocker in selection["blockers"])
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiments", type=Path, default=DEFAULT_EXPERIMENTS)
    parser.add_argument("--candidate")
    parser.add_argument("--variant")
    parser.add_argument("--index", type=int)
    parser.add_argument("--base-url")
    parser.add_argument("--json-output", type=Path, default=DEFAULT_SELECTION_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_SELECTION_MD)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-local-run", action="store_true")
    args = parser.parse_args()

    experiments = load_experiments(args.experiments)
    experiment = select_experiment(experiments, args.candidate, args.variant, args.index)
    command = command_with_overrides(str(experiment["command"]), args.base_url)
    selection = build_selection(experiment, command, args.execute, args.confirm_local_run)

    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(selection, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(selection), encoding="utf-8")
    print(json.dumps(selection, indent=2, ensure_ascii=False))

    if args.execute and selection["blockers"]:
        return 2
    if args.execute:
        result = subprocess.run(command, shell=True, executable="/bin/zsh", cwd=ROOT, check=False)
        return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
