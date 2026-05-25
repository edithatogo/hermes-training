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
            "LOCAL_SERVER_ENDPOINT",
            "LOCAL_SERVER_PORT",
            f"{SSD_EVAL_ROOT}/bfcl/",
        ),
        forbidden=(
            "python -m bfcl_eval",
            "--category simple,multiple,parallel",
            "--limit 25",
        ),
    ),
    ManifestRule(
        rel_path="reports/benchmark/manifests/lm-eval-smoke-command-20260524.md",
        required=(
            f"{GENERAL_ENV}/bin/lm_eval run",
            "local-chat-completions",
            f"{SSD_EVAL_ROOT}/lm-eval/",
        ),
    ),
    ManifestRule(
        rel_path="reports/benchmark/manifests/lm-eval-candidate-command-20260524.md",
        required=(
            f"{GENERAL_ENV}/bin/lm_eval run",
            "arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande",
            f"{SSD_EVAL_ROOT}/lm-eval/",
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
