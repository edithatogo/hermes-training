#!/usr/bin/env python3
"""Build a prompt/profile repair execution ledger from queue and experiment reports."""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from build_prompt_profile_repair_experiments import DEFAULT_OUTPUT as DEFAULT_EXPERIMENTS_STEM
from build_prompt_profile_repair_experiments import base_runner
from build_prompt_profile_repair_queue import DEFAULT_OUTPUT as DEFAULT_QUEUE_STEM


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE_JSON = DEFAULT_QUEUE_STEM.with_suffix(".json")
DEFAULT_EXPERIMENTS_JSON = DEFAULT_EXPERIMENTS_STEM.with_suffix(".json")
DEFAULT_RESULTS_JSON = ROOT / "reports/benchmark/coverage/prompt-profile-repair-results-20260614.json"
DEFAULT_OUTPUT = ROOT / "reports/benchmark/coverage/prompt-profile-repair-ledger-20260614"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def result_key(candidate: str, variant: str) -> str:
    return f"{candidate}\0{variant}"


def candidate_status(
    row: dict[str, Any],
    experiments: list[dict[str, Any]],
    result: dict[str, Any] | None = None,
) -> tuple[str, str]:
    if result:
        return str(result.get("status", "completed")), str(result.get("next_action", "review result report"))
    runner = base_runner(row)
    if runner == "blocked":
        return "blocked-non-local", "candidate environment is not locally runnable; wait for the relevant cloud/offload track"
    if runner == "endpoint":
        return "pending-endpoint", "start the existing local endpoint for the SSD-backed artifact, then run one experiment"
    if runner == "local":
        if any(not item.get("raw_output_promotion_allowed", True) for item in experiments):
            return "pending-local-with-analysis-variant", "run raw-output variants first; analysis-only normalizer variants cannot promote"
        return "pending-local", "run one local MLX/Transformers experiment and capture the report path"
    return "blocked-unknown-runner", f"unknown runner: {runner}"


def build_ledger(
    queue_rows: list[dict[str, Any]],
    experiments: list[dict[str, Any]],
    results: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    by_candidate: dict[str, list[dict[str, Any]]] = {}
    for experiment in experiments:
        by_candidate.setdefault(str(experiment.get("candidate", "")), []).append(experiment)
    by_result = {
        result_key(str(item.get("candidate", "")), str(item.get("variant", ""))): item
        for item in (results or [])
        if isinstance(item, dict)
    }
    results_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for result in results or []:
        if isinstance(result, dict):
            results_by_candidate.setdefault(str(result.get("candidate", "")), []).append(result)

    rows: list[dict[str, Any]] = []
    for index, row in enumerate(queue_rows, 1):
        candidate = str(row.get("id", ""))
        candidate_experiments = sorted(
            by_candidate.get(candidate, []),
            key=lambda item: (int(item.get("priority", 99)), str(item.get("variant", ""))),
        )
        candidate_results = [
            by_result[result_key(candidate, str(item.get("variant", "")))]
            for item in candidate_experiments
            if result_key(candidate, str(item.get("variant", ""))) in by_result
        ]
        matched_result = max(
            candidate_results,
            key=lambda item: float(item.get("pass_rate", -1) or -1),
            default=None,
        )
        candidate_variant_names = {str(item.get("variant", "")) for item in candidate_experiments}
        latest_result = next(
            (
                item
                for item in reversed(results_by_candidate.get(candidate, []))
                if str(item.get("variant", "")) in candidate_variant_names
            ),
            None,
        )
        status, next_action = candidate_status(row, candidate_experiments, matched_result)
        if latest_result and len(candidate_results) == len(candidate_experiments):
            next_action = str(latest_result.get("next_action", next_action))
        rows.append(
            {
                "priority": index,
                "candidate": candidate,
                "environment": row.get("environment", ""),
                "blocked_reason": row.get("blocked_reason", ""),
                "status": status,
                "next_action": next_action,
                "experiments": [
                    {
                        "variant": item.get("variant", ""),
                        "runner": item.get("runner", ""),
                        "raw_output_promotion_allowed": item.get("raw_output_promotion_allowed", False),
                        "strict_scoring": item.get("strict_scoring", False),
                    }
                    for item in candidate_experiments
                ],
                "completed_variants": [str(item.get("variant", "")) for item in candidate_results],
                "result_reports": [
                    str(item.get("result_report", ""))
                    for item in candidate_results
                    if item.get("result_report")
                ],
                "result_report": str(matched_result.get("result_report", "")) if matched_result else "",
                "source_summary": str(matched_result.get("source_summary", "")) if matched_result else "",
                "pass_rate": matched_result.get("pass_rate") if matched_result else None,
                "promotion_gate": "Do not promote until raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, rollback, and publication checks.",
            }
        )
    return rows


def render_markdown(rows: list[dict[str, Any]], run_id: str, created_at: str) -> str:
    lines = [
        "# Prompt/Profile Repair Execution Ledger",
        "",
        f"Run ID: `{run_id}`",
        f"Created: `{created_at}`",
        "",
        "Purpose: track which prompt/profile repair candidates are runnable locally, endpoint-gated, or blocked before execution.",
        "",
        "## Ledger",
        "",
        "| Priority | Candidate | Environment | Status | Experiments | Next action |",
        "|---:|---|---|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['priority']} | `{row['candidate']}` | `{row['environment']}` | `{row['status']}` | {len(row['experiments'])} | {row['next_action']} |"
        )
    lines.extend(
        [
            "",
            "## Gates",
            "",
            "- Run one experiment at a time and write result reports under the SSD-backed evaluation root.",
            "- Leave `result_report` blank until a real benchmark report exists; completed rows must point to a tracked report.",
            "- `pending-endpoint` means a local OpenAI-compatible endpoint must be started manually for the existing artifact.",
            "- `blocked-non-local` is not runnable on this Mac lane; use the matching cloud/offload track.",
            "- Analysis-only normalizer variants can diagnose formatting but cannot promote a candidate.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue-json", type=Path, default=DEFAULT_QUEUE_JSON)
    parser.add_argument("--experiments-json", type=Path, default=DEFAULT_EXPERIMENTS_JSON)
    parser.add_argument("--results-json", type=Path, default=DEFAULT_RESULTS_JSON)
    parser.add_argument("--output-stem", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--created-at")
    args = parser.parse_args()

    queue_rows = load_json(args.queue_json).get("rows", [])
    experiments = load_json(args.experiments_json).get("experiments", [])
    results = load_json(args.results_json).get("results", []) if args.results_json.exists() else []
    if not isinstance(queue_rows, list) or not isinstance(experiments, list) or not isinstance(results, list):
        raise ValueError("queue rows, experiments, and results must be lists")

    rows = build_ledger(
        [row for row in queue_rows if isinstance(row, dict)],
        [item for item in experiments if isinstance(item, dict)],
        [item for item in results if isinstance(item, dict)],
    )
    created_at = args.created_at or datetime.now(UTC).isoformat()
    run_id = args.output_stem.name
    payload = {
        "run_id": run_id,
        "created_at": created_at,
        "source_queue": str(args.queue_json),
        "source_experiments": str(args.experiments_json),
        "source_results": str(args.results_json),
        "rows": rows,
    }
    args.output_stem.parent.mkdir(parents=True, exist_ok=True)
    json_path = args.output_stem.with_suffix(".json")
    md_path = args.output_stem.with_suffix(".md")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(rows, run_id, created_at), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "rows": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
