#!/usr/bin/env python3
"""Check MODEL_CANDIDATES.yaml against the Hugging Face Hub."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from huggingface_hub import HfApi


ROOT = Path(__file__).resolve().parents[1]
RADAR = ROOT / "MODEL_CANDIDATES.yaml"
REQUIRED_FIELDS = (
    "id",
    "family",
    "tier",
    "role",
    "environment",
    "feasibility",
    "parameters",
    "architecture",
    "license",
    "first_runtime",
    "first_finetune",
    "notes",
)
ROLES = {
    "local-finetune",
    "local-runtime",
    "cloud-teacher",
    "cloud-finetune",
    "hosted-teacher",
    "retrieval",
    "research-runtime",
    "watchlist",
}
ENVIRONMENTS = {
    "mac-mlx",
    "mac-ollama",
    "mac-lmstudio",
    "azure-cuda",
    "hf-transformers",
    "hosted-api",
    "retrieval",
    "specialist-runtime",
}
FEASIBILITY = {
    "ready",
    "needs-auth",
    "needs-runtime-proof",
    "cloud-only",
    "hosted-preview-only",
    "speculative",
}


def validate_entry(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    repo_id = str(item.get("id", "<missing id>"))
    for field in REQUIRED_FIELDS:
        if field not in item:
            errors.append(f"{repo_id}: missing {field}")

    role = item.get("role")
    environment = item.get("environment")
    feasibility = item.get("feasibility")
    if role is not None and role not in ROLES:
        errors.append(f"{repo_id}: invalid role {role}")
    if environment is not None and environment not in ENVIRONMENTS:
        errors.append(f"{repo_id}: invalid environment {environment}")
    if feasibility is not None and feasibility not in FEASIBILITY:
        errors.append(f"{repo_id}: invalid feasibility {feasibility}")
    if role == "watchlist" and feasibility != "speculative":
        errors.append(f"{repo_id}: watchlist entries must be speculative")
    if environment == "retrieval" and role != "retrieval":
        errors.append(f"{repo_id}: retrieval environment requires retrieval role")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema-only",
        action="store_true",
        help="Validate local YAML structure without querying Hugging Face.",
    )
    args = parser.parse_args()

    data = yaml.safe_load(RADAR.read_text(encoding="utf-8"))
    candidates = data.get("candidates", [])
    if not isinstance(candidates, list):
        print("schema: candidates must be a list")
        return 1

    api = None if args.schema_only else HfApi()
    failed = False

    for item in candidates:
        if not isinstance(item, dict):
            failed = True
            print("schema: candidate entry is not an object")
            continue
        schema_errors = validate_entry(item)
        if schema_errors:
            failed = True
            for error in schema_errors:
                print(f"schema: {error}")
            continue
        if args.schema_only:
            continue

        repo_id = item["id"]
        role = item.get("role", "")
        feasibility = item.get("feasibility", "")
        print(f"\n== {repo_id}")
        if feasibility == "hosted-preview-only":
            print("skipped: hosted preview without open weights")
            continue
        if role == "watchlist" or feasibility == "speculative":
            print("skipped: watchlist/speculative entry")
            continue
        try:
            info = api.model_info(repo_id)
        except Exception as exc:  # noqa: BLE001
            failed = True
            print(f"missing: {type(exc).__name__}: {str(exc).splitlines()[0]}")
            continue

        tags = ",".join((info.tags or [])[:12])
        print("exists: yes")
        print(f"private: {info.private}")
        print(f"downloads: {info.downloads}")
        print(f"likes: {info.likes}")
        print(f"modified: {info.lastModified}")
        print(f"tags: {tags}")

    if args.schema_only and not failed:
        print(f"schema ok: {len(candidates)} root model candidates")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
