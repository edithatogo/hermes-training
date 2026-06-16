#!/usr/bin/env python3
"""Build the remaining official-candidate benchmark execution queue.

This report is intentionally fail-closed: it records what is missing and how to
run it, but does not promote coverage or create benchmark scores.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COVERAGE = ROOT / "reports/benchmark/standard-coverage/qwen3-v4-targeted-standard-coverage-20260526.json"
DEFAULT_JSON = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.json"
DEFAULT_MD = ROOT / "reports/benchmark/official-candidates/qwen3-v4-official-candidate-suite-queue-20260616.md"
SSD_ROOT = "/Volumes/PortableSSD/hermes-evals/standard-benchmarks"
BFCL_ENV = "/Volumes/PortableSSD/hermes-training-envs/bfcl-py312"
GENERAL_ENV = "/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312"
ADAPTER = "gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter"
PEFT_REPO = "edithatogo/qwen3-4b-hermes-lora-peft-converted"
BASE_MODEL = "Qwen/Qwen3-4B"


@dataclass(frozen=True)
class SuiteQueueItem:
    suite: str
    status: str
    priority: int
    blocker: str
    next_action: str
    run_id: str
    output_root: str
    local_command: str
    cloud_command: str
    completion_criteria: list[str]
    publication_boundary: str = "No public broad benchmark claim until this suite has scored artifacts and review sign-off."


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def missing_suites(coverage: dict[str, Any]) -> set[str]:
    missing = coverage.get("official_candidate_missing")
    if missing is None:
        missing = coverage.get("summary", {}).get("official_candidate_missing", [])
    return {str(item) for item in missing}


def build_items(coverage_path: Path) -> list[SuiteQueueItem]:
    coverage = load_json(coverage_path)
    missing = missing_suites(coverage)

    definitions = [
        SuiteQueueItem(
            suite="official-bfcl",
            status="missing" if "official-bfcl" in missing else "present",
            priority=10,
            blocker="Needs a local OpenAI-compatible endpoint for the v4 PEFT adapter or a cloud endpoint that supports BFCL self-hosted generation.",
            next_action="Start the v4 adapter endpoint, then run the isolated BFCL env against simple_python,multiple,parallel before broad BFCL categories.",
            run_id="qwen3-v4-peft-official-bfcl-20260616",
            output_root=f"{SSD_ROOT}/bfcl/qwen3-v4-peft-official-bfcl-20260616",
            local_command=(
                f"REMOTE_OPENAI_BASE_URL=http://127.0.0.1:<port>/v1 REMOTE_OPENAI_API_KEY=EMPTY "
                f"{BFCL_ENV}/bin/bfcl generate --model Qwen/Qwen3-4B-Instruct-2507-FC "
                "--test-category simple_python,multiple,parallel --temperature 0 --skip-server-setup "
                f"--result-dir {SSD_ROOT}/bfcl/qwen3-v4-peft-official-bfcl-20260616/results --include-input-log && "
                f"{BFCL_ENV}/bin/bfcl evaluate --model Qwen/Qwen3-4B-Instruct-2507-FC "
                "--test-category simple_python,multiple,parallel "
                f"--result-dir {SSD_ROOT}/bfcl/qwen3-v4-peft-official-bfcl-20260616/results "
                f"--score-dir {SSD_ROOT}/bfcl/qwen3-v4-peft-official-bfcl-20260616/scores --partial-eval"
            ),
            cloud_command="Route the same OpenAI-compatible endpoint command through a persistent backend only after its operator gate passes.",
            completion_criteria=[
                "BFCL generate returns 0",
                "BFCL evaluate returns 0",
                "score directory contains category summaries",
                "run card records endpoint, adapter revision, raw result root, and errors",
            ],
        ),
        SuiteQueueItem(
            suite="official-coding",
            status="missing" if "official-coding" in missing else "present",
            priority=20,
            blocker="Needs an execution-enabled coding harness path; generation-only results must not be reported as pass@k.",
            next_action="Use EvalPlus/HumanEval/MBPP from the general benchmark env with execution enabled, or record the sandbox blocker explicitly.",
            run_id="qwen3-v4-peft-official-coding-20260616",
            output_root=f"{SSD_ROOT}/coding/qwen3-v4-peft-official-coding-20260616",
            local_command=(
                f"{GENERAL_ENV}/bin/python -m evalplus.evaluate humaneval "
                f"--samples {SSD_ROOT}/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl "
                "--test-details"
            ),
            cloud_command=(
                "Use a persistent GPU/CPU container only after sandbox, result persistence, and cost gates are recorded."
            ),
            completion_criteria=[
                "generated solutions are saved before execution",
                "test execution is enabled and recorded",
                "pass@1, compile errors, and timeouts are summarized",
                "run card records sandbox and raw generated solution paths",
            ],
        ),
        SuiteQueueItem(
            suite="safety-refusal",
            status="missing" if "safety-refusal" in missing else "present",
            priority=30,
            blocker="Needs a pinned refusal/safety suite with expected refusal boundaries for unavailable or disallowed tools.",
            next_action="Materialize a versioned refusal suite from the held-out refusal cases plus unsafe-tool prompts, then score exact JSON refusal behavior.",
            run_id="qwen3-v4-peft-safety-refusal-20260616",
            output_root=f"{SSD_ROOT}/safety/qwen3-v4-peft-safety-refusal-20260616",
            local_command=(
                "./.venv/bin/python scripts/run_tool_call_benchmark.py "
                "--suite reports/benchmark/manifests/safety-refusal-suite-20260616.json "
                f"--output-dir {SSD_ROOT}/safety/qwen3-v4-peft-safety-refusal-20260616"
            ),
            cloud_command="No cloud execution needed unless local runtime cannot serve the adapter reliably.",
            completion_criteria=[
                "suite manifest is versioned",
                "all refusal cases preserve plain-text no-tool-call refusals",
                "unsafe or unavailable tools are refused without leaking forbidden calls",
                "run card includes failure examples",
            ],
        ),
        SuiteQueueItem(
            suite="ruler-long-context",
            status="missing" if "ruler-long-context" in missing else "present",
            priority=40,
            blocker="Needs a context-length decision and a RULER-compatible runtime path; local Mac runs may be slow or memory-bound.",
            next_action="Start with a small RULER needle/retrieval slice at the actual supported context length, then scale only if the runtime is stable.",
            run_id="qwen3-v4-peft-ruler-long-context-20260616",
            output_root=f"{SSD_ROOT}/ruler/qwen3-v4-peft-ruler-long-context-20260616",
            local_command=(
                f"{GENERAL_ENV}/bin/lm_eval run --model hf "
                f"--model_args pretrained={BASE_MODEL},peft={PEFT_REPO},trust_remote_code=True,dtype=float16,device=mps "
                "--tasks niah_single_1 --batch_size 1 "
                f"--output_path {SSD_ROOT}/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096"
            ),
            cloud_command="Prefer Kaggle/Modal/Azure only after a persistent backend gate passes and the context length fits GPU memory.",
            completion_criteria=[
                "context length/task and tokenizer settings are recorded",
                "RULER task outputs are saved",
                "score summary includes task accuracy and context length",
                "run card records memory/runtime failures if blocked",
            ],
        ),
    ]
    return definitions


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qwen3 v4 Official Candidate Suite Queue",
        "",
        f"Coverage source: `{report['coverage_source']}`",
        f"Adapter: `{ADAPTER}`",
        f"PEFT repo: `{PEFT_REPO}`",
        "",
        "This queue keeps missing official-candidate suites executable without treating them as completed evidence.",
        "",
        "| Suite | Status | Priority | Blocker | Next action |",
        "|---|---:|---:|---|---|",
    ]
    for item in report["items"]:
        lines.append(
            f"| `{item['suite']}` | `{item['status']}` | {item['priority']} | "
            f"{item['blocker']} | {item['next_action']} |"
        )
    lines.extend(["", "## Commands", ""])
    for item in report["items"]:
        lines.extend(
            [
                f"### {item['suite']}",
                "",
                f"- Run ID: `{item['run_id']}`",
                f"- Output root: `{item['output_root']}`",
                f"- Publication boundary: {item['publication_boundary']}",
                "",
                "Local command:",
                "",
                "```bash",
                item["local_command"],
                "```",
                "",
                f"Cloud route: {item['cloud_command']}",
                "",
                "Completion criteria:",
            ]
        )
        for criterion in item["completion_criteria"]:
            lines.append(f"- {criterion}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_report(coverage_path: Path) -> dict[str, Any]:
    items = [asdict(item) for item in build_items(coverage_path)]
    missing = [item["suite"] for item in items if item["status"] == "missing"]
    try:
        coverage_source = str(coverage_path.relative_to(ROOT))
    except ValueError:
        coverage_source = str(coverage_path)
    return {
        "coverage_source": coverage_source,
        "candidate": "qwen3-4b-strict-toolcall-v4-targeted",
        "base_model": BASE_MODEL,
        "adapter": ADAPTER,
        "peft_repo": PEFT_REPO,
        "status": "blocked-missing-official-candidates" if missing else "complete",
        "missing_suites": missing,
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    report = build_report(args.coverage)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"status": report["status"], "missing_suites": report["missing_suites"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
