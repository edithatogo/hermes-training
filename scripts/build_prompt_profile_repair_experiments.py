#!/usr/bin/env python3
"""Build concrete prompt/profile repair experiment commands from the repair queue."""
from __future__ import annotations

import argparse
import json
import shlex
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from scripts.build_prompt_profile_repair_queue import DEFAULT_OUTPUT as DEFAULT_QUEUE_STEM, slugify
except ModuleNotFoundError:  # pragma: no cover - direct script execution path
    from build_prompt_profile_repair_queue import DEFAULT_OUTPUT as DEFAULT_QUEUE_STEM, slugify


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE_JSON = DEFAULT_QUEUE_STEM.with_suffix(".json")
DEFAULT_OUTPUT = ROOT / "reports/benchmark/coverage/prompt-profile-repair-experiments-20260614"
STRICT_SUFFIX = (
    " Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. "
    "If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available."
)
COPY_EXACT_SUFFIX = " Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments."
EMPTY_RETRY_SUFFIX = " If a listed tool can satisfy the request, emit the tool call instead of an empty answer."
QWEN_PREFILL = "<think>\n\n</think>\n\n"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def quote(value: str) -> str:
    if "${RUN_STAMP}" in value:
        return value
    return shlex.quote(value)


def base_runner(row: dict[str, Any]) -> str:
    environment = str(row.get("environment", ""))
    model_id = str(row.get("id", ""))
    if environment not in {"mac-mlx", "mac-lmstudio", "mac-ollama", "hf-transformers"}:
        return "blocked"
    route_text = " ".join(
        str(row.get(key, ""))
        for key in ("id", "environment", "repair_hypothesis", "next_command")
    ).lower()
    if "run_endpoint_pilot_benchmark.py" in route_text or "gguf" in route_text or environment in {"mac-lmstudio", "mac-ollama"}:
        return "endpoint"
    return "local"


def command_for(row: dict[str, Any], variant: dict[str, str]) -> str:
    model_id = str(row["id"])
    slug = slugify(model_id)
    variant_id = variant["id"]
    runner = base_runner(row)
    common = [
        "source scripts/env.sh",
        "RUN_STAMP=$(date +%Y%m%d-%H%M%S)",
        "# No download here: run only against the existing SSD-backed artifact or local endpoint.",
    ]
    if runner == "endpoint":
        command = [
            "./.venv/bin/python",
            "scripts/run_endpoint_pilot_benchmark.py",
            "--model",
            slug,
            "--base-url",
            "http://127.0.0.1:<port>/v1",
            "--suite",
            "benchmarks/endpoint_pilots/bfcl_pilot.json",
            "--max-tokens",
            variant.get("max_tokens", "512"),
            "--require-no-extra-tool-text",
            "--run-id",
            f"{slug}-{variant_id}-${{RUN_STAMP}}",
        ]
    else:
        command = [
            "./.venv/bin/python",
            "scripts/run_local_pilot_benchmark.py",
            "--model",
            model_id,
            "--suite",
            "benchmarks/endpoint_pilots/bfcl_pilot.json",
            "--max-tokens",
            variant.get("max_tokens", "512"),
            "--require-no-extra-tool-text",
            "--run-id",
            f"{slug}-{variant_id}-${{RUN_STAMP}}",
        ]
    for flag, key in (
        ("--system-prefix", "system_prefix"),
        ("--system-suffix", "system_suffix"),
        ("--user-prefix", "user_prefix"),
        ("--assistant-prefill", "assistant_prefill"),
        ("--score-normalizer", "score_normalizer"),
    ):
        value = variant.get(key, "")
        if value:
            command.extend([flag, value])
    return "\n".join([*common, " ".join(quote(part) for part in command)])


def variants_for(row: dict[str, Any]) -> list[dict[str, str]]:
    model_text = " ".join(str(row.get(key, "")) for key in ("id", "family", "blocked_reason")).lower()
    runner = base_runner(row)
    variants = [
        {
            "id": "strict-suffix-copy-exact",
            "goal": "tighten raw Hermes tool-call formatting and exact argument copying",
            "system_suffix": STRICT_SUFFIX + COPY_EXACT_SUFFIX,
            "max_tokens": "512",
        }
    ]
    if "empty/no-content" in model_text:
        variants.append(
            {
                "id": "empty-output-retry",
                "goal": "test whether a direct non-empty tool-call instruction clears strict-prompt blank output",
                "system_suffix": STRICT_SUFFIX + EMPTY_RETRY_SUFFIX,
                "max_tokens": "512",
            }
        )
    if "qwen" in model_text:
        variants.append(
            {
                "id": "qwen-no-think-prefill",
                "goal": "test Qwen no-think controls while preserving strict no-extra-tool-text scoring",
                "user_prefix": "/no_think",
                "assistant_prefill": QWEN_PREFILL,
                "system_suffix": STRICT_SUFFIX + COPY_EXACT_SUFFIX,
                "max_tokens": "512",
            }
        )
    if "gemma" in model_text and runner == "local":
        variants.append(
            {
                "id": "gemma-native-normalizer-analysis",
                "goal": "measure score-only Gemma native tool-fragment normalization without changing raw-output promotion rules",
                "system_suffix": STRICT_SUFFIX + COPY_EXACT_SUFFIX,
                "score_normalizer": "gemma-native-tool-call",
                "max_tokens": "512",
            }
        )
    if "granite" in model_text and runner == "local":
        variants.append(
            {
                "id": "granite-native-normalizer-analysis",
                "goal": "measure score-only Granite native tool-call normalization and exact-copy repair",
                "system_suffix": STRICT_SUFFIX + COPY_EXACT_SUFFIX,
                "score_normalizer": "granite-native-tool-call",
                "max_tokens": "512",
            }
        )
    if "minicpm" in model_text:
        variants.append(
            {
                "id": "minicpm-empty-tag-repair",
                "goal": "test a concise tool-tag envelope for MiniCPM helper candidates before any promotion claim",
                "system_suffix": STRICT_SUFFIX + " Use one concise <tool_call> block and no commentary.",
                "max_tokens": "384",
            }
        )
    return variants


def build_experiments(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    experiments: list[dict[str, Any]] = []
    for row in rows:
        candidate = str(row.get("id", ""))
        runner = base_runner(row)
        if runner == "blocked":
            continue
        for priority, variant in enumerate(variants_for(row), 1):
            if runner == "endpoint" and variant.get("score_normalizer"):
                continue
            experiments.append(
                {
                    "candidate": candidate,
                    "environment": row.get("environment", ""),
                    "blocked_reason": row.get("blocked_reason", ""),
                    "variant": variant["id"],
                    "goal": variant["goal"],
                    "runner": runner,
                    "strict_scoring": True,
                    "raw_output_promotion_allowed": not variant["id"].endswith("-analysis"),
                    "promotion_boundary": "A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.",
                    "command": command_for(row, variant),
                    "priority": priority,
                }
            )
    experiments.sort(key=lambda item: (str(item["candidate"]), int(item["priority"]), str(item["variant"])))
    return experiments


def render_markdown(experiments: list[dict[str, Any]], run_id: str, created_at: str) -> str:
    lines = [
        "# Prompt/Profile Repair Experiments",
        "",
        f"Run ID: `{run_id}`",
        f"Created: `{created_at}`",
        "",
        "Purpose: turn the prompt/profile repair queue into concrete, no-download experiment commands using existing local runners.",
        "",
        "## Matrix",
        "",
        "| Candidate | Variant | Runner | Raw-output promotion allowed | Goal |",
        "|---|---|---|---|---|",
    ]
    for experiment in experiments:
        allowed = "yes" if experiment["raw_output_promotion_allowed"] else "no; analysis only"
        lines.append(
            f"| `{experiment['candidate']}` | `{experiment['variant']}` | `{experiment['runner']}` | {allowed} | {experiment['goal']} |"
        )
    lines.extend(["", "## Command Templates", ""])
    for experiment in experiments[:24]:
        lines.extend(
            [
                f"### {experiment['candidate']} / {experiment['variant']}",
                "",
                f"- Goal: {experiment['goal']}",
                f"- Boundary: {experiment['promotion_boundary']}",
                "",
                "```bash",
                str(experiment["command"]),
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "## Policy",
            "",
            "- Do not redownload models from these commands.",
            "- Keep score-only normalizer variants out of raw-output promotion decisions.",
            "- Every command keeps `--require-no-extra-tool-text` enabled.",
            "- Treat endpoint `<port>` placeholders as operator-supplied local runtime state, not a default service assumption.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue-json", type=Path, default=DEFAULT_QUEUE_JSON)
    parser.add_argument("--output-stem", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--created-at")
    args = parser.parse_args()

    queue = load_json(args.queue_json)
    rows = queue.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError("queue rows must be a list")
    experiments = build_experiments([row for row in rows if isinstance(row, dict)])
    created_at = args.created_at or datetime.now(UTC).isoformat()
    run_id = args.output_stem.name
    payload = {
        "run_id": run_id,
        "created_at": created_at,
        "source_queue": str(args.queue_json),
        "experiments": experiments,
    }
    args.output_stem.parent.mkdir(parents=True, exist_ok=True)
    json_path = args.output_stem.with_suffix(".json")
    md_path = args.output_stem.with_suffix(".md")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(experiments, run_id, created_at), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "experiments": len(experiments)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
