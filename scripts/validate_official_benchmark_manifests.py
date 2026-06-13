#!/usr/bin/env python3
"""Validate lightweight official benchmark command manifests.

This is a static/readiness check. It does not launch benchmark runs, contact
model endpoints, download benchmark data, or write benchmark artifacts.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_ROOT = ROOT / "reports" / "benchmark" / "manifests"
SSD_EVAL_ROOT = "/Volumes/PortableSSD/hermes-evals/standard-benchmarks"
BFCL_ENV = "/Volumes/PortableSSD/hermes-training-envs/bfcl-py312"
GENERAL_ENV = "/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312"


@dataclass(frozen=True)
class ManifestRule:
    rel_path: str
    required: tuple[str, ...]
    forbidden: tuple[str, ...] = ()

    @property
    def path(self) -> Path:
        return ROOT / self.rel_path


@dataclass(frozen=True)
class ScorecardPlanRule:
    rel_path: str
    run_id: str
    required_tasks: tuple[str, ...]
    output_prefix: str = f"{SSD_EVAL_ROOT}/lm-eval/"

    @property
    def path(self) -> Path:
        return ROOT / self.rel_path


RULES = (
    ManifestRule(
        rel_path="reports/benchmark/manifests/bfcl-pilot-command-20260524.md",
        required=(
            f"{BFCL_ENV}/bin/bfcl generate",
            f"{BFCL_ENV}/bin/bfcl evaluate",
            "--skip-server-setup",
            "REMOTE_OPENAI_BASE_URL",
            "REMOTE_OPENAI_API_KEY",
            "Qwen/Qwen3-4B-Instruct-2507-FC",
            f"{SSD_EVAL_ROOT}/bfcl/",
        ),
        forbidden=(
            "python -m bfcl_eval",
            "LOCAL_SERVER_ENDPOINT",
            "LOCAL_SERVER_PORT",
            "--category simple,multiple,parallel",
            "--limit 25",
        ),
    ),
    ManifestRule(
        rel_path="reports/benchmark/manifests/lm-eval-smoke-command-20260524.md",
        required=(
            f"{GENERAL_ENV}/bin/python scripts/run_mlx_lm_eval.py",
            "--limit 10",
            "qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit10-<date>",
            f"{SSD_EVAL_ROOT}/lm-eval/",
        ),
        forbidden=(
            "--model local-chat-completions",
            "base_url=http://127.0.0.1:8080/v1/chat/completions",
        ),
    ),
    ManifestRule(
        rel_path="reports/benchmark/manifests/lm-eval-candidate-command-20260524.md",
        required=(
            f"{GENERAL_ENV}/bin/python scripts/run_mlx_lm_eval.py",
            "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande",
            "Qwen/Qwen3-4B-MLX-4bit",
            f"{SSD_EVAL_ROOT}/lm-eval/",
        ),
        forbidden=(
            "--model local-chat-completions",
            "base_url=http://127.0.0.1:8080/v1/chat/completions",
        ),
    ),
)

SCORECARD_PLAN_RULES = (
    ScorecardPlanRule(
        rel_path="reports/benchmark/manifests/lm-eval-full-scorecard-plan-20260613.yaml",
        run_id="qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613",
        required_tasks=("arc_challenge", "hellaswag", "truthfulqa_mc2", "gsm8k", "winogrande"),
    ),
)


def collapse(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def validate_manifest(rule: ManifestRule) -> list[str]:
    errors: list[str] = []
    if not rule.path.exists():
        return [f"missing {rule.rel_path}"]

    text = rule.path.read_text(encoding="utf-8")
    normalized = collapse(text)
    for needle in rule.required:
        if needle not in text and needle not in normalized:
            errors.append(f"{rule.rel_path}: missing required text `{needle}`")
    for needle in rule.forbidden:
        if needle in text or needle in normalized:
            errors.append(f"{rule.rel_path}: stale/forbidden text `{needle}`")
    return errors


def validate_scorecard_plan(rule: ScorecardPlanRule) -> list[str]:
    errors: list[str] = []
    if not rule.path.exists():
        return [f"missing {rule.rel_path}"]

    try:
        plan = yaml.safe_load(rule.path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"{rule.rel_path}: invalid YAML: {exc}"]
    if not isinstance(plan, dict):
        return [f"{rule.rel_path}: plan must be a mapping"]

    if plan.get("run_id") != rule.run_id:
        errors.append(f"{rule.rel_path}: run_id must be `{rule.run_id}`")
    if plan.get("suite") != "lm-eval-selected":
        errors.append(f"{rule.rel_path}: suite must be `lm-eval-selected`")
    if plan.get("status") not in {"planned", "running", "blocked", "scored"}:
        errors.append(f"{rule.rel_path}: status must be planned, running, blocked, or scored")
    if plan.get("publish_boundary") != "internal-candidate":
        errors.append(f"{rule.rel_path}: publish_boundary must be `internal-candidate` until full review")
    if plan.get("limit") is not None:
        errors.append(f"{rule.rel_path}: full scorecard plan must use limit: null")
    if str(plan.get("model", "")) != "Qwen/Qwen3-4B-MLX-4bit":
        errors.append(f"{rule.rel_path}: model must remain the v4 MLX base for this plan")
    if str(plan.get("adapter", "")) != "gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter":
        errors.append(f"{rule.rel_path}: adapter must point to the v4 targeted LoRA")

    tasks = plan.get("tasks")
    if not isinstance(tasks, list) or tuple(tasks) != rule.required_tasks:
        errors.append(f"{rule.rel_path}: tasks must be {list(rule.required_tasks)} in order")

    output_dir = str(plan.get("output_dir", ""))
    artifact_root = str(plan.get("artifact_root", ""))
    if not artifact_root.startswith(SSD_EVAL_ROOT):
        errors.append(f"{rule.rel_path}: artifact_root must be under {SSD_EVAL_ROOT}")
    if not output_dir.startswith(rule.output_prefix):
        errors.append(f"{rule.rel_path}: output_dir must be under {rule.output_prefix}")
    if rule.run_id not in output_dir:
        errors.append(f"{rule.rel_path}: output_dir must include the run_id")

    report = str(plan.get("report", ""))
    if report != f"reports/benchmark/lm-eval/{rule.run_id}.md":
        errors.append(f"{rule.rel_path}: report path must match the run_id")

    command = str(plan.get("command", ""))
    task_arg = ",".join(rule.required_tasks)
    required_command_text = (
        f"--run-id {rule.run_id}",
        "scripts/run_mlx_lm_eval.py",
        f"--tasks {task_arg}",
        "--output-dir \"$OUT\"",
    )
    for needle in required_command_text:
        if needle not in command:
            errors.append(f"{rule.rel_path}: command missing `{needle}`")
    if "--limit" in command:
        errors.append(f"{rule.rel_path}: command must not include --limit for the full selected-task scorecard")

    completion = plan.get("completion_criteria")
    if not isinstance(completion, list) or not completion:
        errors.append(f"{rule.rel_path}: completion_criteria must be a non-empty list")
    else:
        required_completion_text = (
            "summary.json status is scored",
            "results.json contains every selected task",
            "coverage report no longer marks lm-eval-selected missing",
        )
        joined = "\n".join(str(item) for item in completion)
        for needle in required_completion_text:
            if needle not in joined:
                errors.append(f"{rule.rel_path}: completion_criteria missing `{needle}`")

    blocked_claims = plan.get("blocked_public_claims_until_complete")
    if not isinstance(blocked_claims, list) or "full selected-task lm-eval scorecard" not in blocked_claims:
        errors.append(f"{rule.rel_path}: blocked_public_claims_until_complete must block full scorecard claims")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    for rule in RULES:
        errors.extend(validate_manifest(rule))
    for rule in SCORECARD_PLAN_RULES:
        errors.extend(validate_scorecard_plan(rule))

    if errors:
        for error in errors:
            print(f"fail: {error}")
        return 1

    if not args.quiet:
        for rule in RULES:
            print(f"ok: {rule.rel_path}")
        for rule in SCORECARD_PLAN_RULES:
            print(f"ok: {rule.rel_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
