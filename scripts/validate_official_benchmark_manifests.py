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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    for rule in RULES:
        errors.extend(validate_manifest(rule))

    if errors:
        for error in errors:
            print(f"fail: {error}")
        return 1

    if not args.quiet:
        for rule in RULES:
            print(f"ok: {rule.rel_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
