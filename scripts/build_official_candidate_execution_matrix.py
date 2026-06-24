#!/usr/bin/env python3
"""Build the official-candidate execution matrix from queue and preflights."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.json"
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-execution-matrix-20260616.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-execution-matrix-20260616.md"

PREFLIGHTS = {
    "official-bfcl": ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-bfcl-preflight-20260616.json",
    "official-coding": ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-coding-preflight-20260616.json",
    "ruler-long-context": ROOT
    / "reports/benchmark/official-candidates/qwen3-v4-ruler-long-context-preflight-20260616.json",
}
RUNTIME_ATTEMPTS = {
    "official-coding": ROOT
    / "reports/benchmark/official-candidates/qwen3-v4-official-coding-generation-attempt-20260624.json",
    "ruler-long-context": ROOT
    / "reports/benchmark/official-candidates/qwen3-v4-ruler-long-context-runtime-attempt-20260624.json",
}
BFCL_RESULT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-bfcl-result-20260624.json"
CODING_RESULTS = (
    ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-coding-evalplus-rerun-20260624.json",
    ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-coding-evalplus-result-20260624.json",
)
RULER_RESULT = ROOT / "reports/benchmark/official-candidates/qwen3-v4-ruler-ctx4096-full-result-20260624.json"
SAFETY_MANIFEST = ROOT / "reports/benchmark/manifests/safety-refusal-suite-20260616.json"
SAFETY_SUMMARY = Path(
    "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/"
    "qwen3-v4-peft-safety-refusal-20260616/summary.json"
)


@dataclass(frozen=True)
class SuiteExecution:
    suite: str
    queue_status: str
    execution_status: str
    blocker: str
    next_action: str
    output_root: str
    completion_artifact: str
    local_command: str


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def first_existing(paths: tuple[Path, ...]) -> Path | None:
    return next((path for path in paths if path.exists()), None)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def expected_completion_artifact(suite: str, output_root: str) -> str:
    if suite == "official-bfcl":
        return f"{output_root}/scores"
    if suite == "official-coding":
        return f"{output_root}/generated.jsonl and EvalPlus score output"
    if suite == "safety-refusal":
        return f"{output_root}/summary.json"
    if suite == "ruler-long-context":
        return f"{output_root}/ctx4096 score summary"
    return output_root


def suite_status(item: dict[str, Any]) -> tuple[str, str, str]:
    suite = str(item["suite"])
    if suite == "safety-refusal":
        if SAFETY_SUMMARY.exists():
            summary = load_json(SAFETY_SUMMARY)
            return (
                "scored-artifact-present",
                (
                    f"Scored artifact exists; strict pass rate is {float(summary.get('pass_rate', 0.0)):.3f}, "
                    "so this is evidence for repair prioritization rather than a passing safety claim."
                ),
                "Inspect residual refusal failures and add a repair track before public safety/refusal claims.",
            )
        if SAFETY_MANIFEST.exists():
            return (
                "ready-for-runtime",
                "Runtime/model execution is still required; no scored summary exists yet.",
                "Run the pinned suite against the v4 adapter when local runtime is available.",
            )
        return (
            "blocked-preflight",
            "Pinned safety/refusal manifest is missing.",
            "Regenerate the safety/refusal suite manifest.",
        )
    if suite == "official-bfcl" and BFCL_RESULT.exists():
        result = load_json(BFCL_RESULT)
        if result.get("status") == "scored-artifact-present":
            metrics = result["metrics"]
            return (
                "scored-artifact-present",
                (
                    "BFCL selected-slice scored artifact exists; "
                    f"overall accuracy is {float(metrics['overall_acc']):.3f} across simple_python,multiple,parallel."
                ),
                str(result["next_action"]),
            )
    coding_result = first_existing(CODING_RESULTS)
    if suite == "official-coding" and coding_result:
        result = load_json(coding_result)
        if result.get("status") == "scored-artifact-present":
            return (
                "scored-artifact-present",
                (
                    "EvalPlus scored artifact exists; HumanEval base pass@1 is "
                    f"{float(result['evalplus_printed_scores']['humaneval_base_pass_at_1']):.3f} and "
                    "HumanEval+ pass@1 is "
                    f"{float(result['evalplus_printed_scores']['humaneval_plus_pass_at_1']):.3f}."
                ),
                "Inspect failed HumanEval tasks before making any broad coding claim.",
            )
    if suite == "ruler-long-context" and RULER_RESULT.exists():
        result = load_json(RULER_RESULT)
        if result.get("status") == "scored-artifact-present":
            metric = result["metric"]
            return (
                "scored-artifact-present",
                (
                    "Full RULER ctx4096 artifact exists; "
                    f"{metric['task']} {metric['name']} score is {float(metric['value']):.3f} "
                    f"over {int(result['sample_len'])} samples."
                ),
                "Add longer-context RULER slices before making claims beyond ctx4096 needle retrieval.",
            )

    runtime_attempt_path = RUNTIME_ATTEMPTS.get(suite)
    if runtime_attempt_path and runtime_attempt_path.exists():
        runtime_attempt = load_json(runtime_attempt_path)
        if str(runtime_attempt.get("status")).startswith("blocked-runtime"):
            return (
                "blocked-runtime",
                str(runtime_attempt.get("diagnosis") or runtime_attempt.get("blocker", "Runtime attempt is blocked.")),
                str(runtime_attempt.get("next_action", item["next_action"])),
            )

    preflight_path = PREFLIGHTS.get(suite)
    if not preflight_path or not preflight_path.exists():
        return ("blocked-preflight", "Preflight report is missing.", "Regenerate the suite preflight report.")
    preflight = load_json(preflight_path)
    status = str(preflight.get("status", ""))
    blockers = preflight.get("blockers") or []
    blocker_text = "; ".join(str(item) for item in blockers) if blockers else "none"
    if status == "ready-to-run" or status == "ready-to-evaluate":
        return ("ready-for-runtime", "Preflight is ready; scored artifacts are still missing.", str(item["next_action"]))
    return ("blocked-preflight", blocker_text, str(item["next_action"]))


def build_matrix(queue_path: Path = DEFAULT_QUEUE) -> dict[str, Any]:
    queue = load_json(queue_path)
    rows: list[SuiteExecution] = []
    coding_result = first_existing(CODING_RESULTS)
    for item in queue["items"]:
        execution_status, blocker, next_action = suite_status(item)
        output_root = str(item["output_root"])
        completion_artifact = expected_completion_artifact(str(item["suite"]), output_root)
        local_command = str(item["local_command"])
        if str(item["suite"]) == "official-coding" and coding_result:
            result = load_json(coding_result)
            output_root = str(Path(str(result["generated_samples"]["path"])).parent)
            completion_artifact = f"{result['generated_samples']['path']} and {result['result_json']}"
            local_command = str(result["command"])
        if str(item["suite"]) == "official-bfcl" and BFCL_RESULT.exists():
            result = load_json(BFCL_RESULT)
            output_root = str(Path(str(result["artifacts"]["score_root"])).parent)
            completion_artifact = str(result["artifacts"]["overall_csv"])
            local_command = str(result.get("local_command") or local_command)
        rows.append(
            SuiteExecution(
                suite=str(item["suite"]),
                queue_status=str(item["status"]),
                execution_status=execution_status,
                blocker=blocker,
                next_action=next_action,
                output_root=output_root,
                completion_artifact=completion_artifact,
                local_command=local_command,
            )
        )
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.execution_status] = counts.get(row.execution_status, 0) + 1
    all_scored = counts.get("scored-artifact-present", 0) == len(rows)
    return {
        "candidate": queue["candidate"],
        "adapter": queue["adapter"],
        "queue_source": display_path(queue_path),
        "status": "scored-artifacts-present-repair-required" if all_scored else "blocked-pending-scored-artifacts",
        "counts": counts,
        "rows": [row.__dict__ for row in rows],
        "publication_boundary": (
            "No public broad benchmark claim until every required suite has scored artifacts and the scored gates pass, "
            "or until failures are explicitly excluded in publication materials."
        ),
    }


def render_markdown(matrix: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 v4 Official Candidate Execution Matrix",
        "",
        f"Candidate: `{matrix['candidate']}`",
        f"Adapter: `{matrix['adapter']}`",
        f"Queue source: `{matrix['queue_source']}`",
        f"Status: `{matrix['status']}`",
        "",
        matrix["publication_boundary"],
        "",
        "| Suite | Queue | Execution | Blocker | Completion artifact |",
        "|---|---|---|---|---|",
    ]
    for row in matrix["rows"]:
        lines.append(
            f"| `{row['suite']}` | `{row['queue_status']}` | `{row['execution_status']}` | "
            f"{row['blocker']} | `{row['completion_artifact']}` |"
        )
    lines.extend(["", "## Next Actions", ""])
    for row in matrix["rows"]:
        lines.extend(
            [
                f"### {row['suite']}",
                "",
                f"- Next action: {row['next_action']}",
                f"- Output root: `{row['output_root']}`",
                "",
                "```bash",
                row["local_command"],
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    matrix = build_matrix(args.queue)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(matrix), encoding="utf-8")
    print(json.dumps({"status": matrix["status"], "counts": matrix["counts"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
