#!/usr/bin/env python3
"""Validate mem0/MODEL_CANDIDATES.yaml and optionally check Hugging Face repos."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from huggingface_hub import HfApi


ROOT = Path(__file__).resolve().parents[1]
RADAR = ROOT / "mem0" / "MODEL_CANDIDATES.yaml"
REQUIRED_FIELDS = ("id", "role", "family", "runtime", "embedding_dims", "status", "first_gate", "notes")
ROLES = {"extractor", "embedder", "reranker", "retriever", "summarizer"}
STATUSES = {
    "working-default",
    "working-default-clean-root-smoked",
    "installed-baseline",
    "candidate",
    "planned",
    "runtime-proof-needed",
    "benchmarked-cpu-mps-not-promoted",
    "candidate-runtime-id-verified",
    "source-model-benchmarked",
    "live-read-wrapper-smoked",
    "rejected",
}


def is_hf_repo(model_id: str) -> bool:
    return "/" in model_id and ":" not in model_id


def validate_candidate(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    model_id = str(item.get("id", "<missing id>"))
    for field in REQUIRED_FIELDS:
        if field not in item:
            errors.append(f"{model_id}: missing {field}")
    role = item.get("role")
    if role is not None and role not in ROLES:
        errors.append(f"{model_id}: invalid role {role}")
    runtime = item.get("runtime")
    if runtime is not None and (not isinstance(runtime, list) or not all(isinstance(value, str) for value in runtime)):
        errors.append(f"{model_id}: runtime must be a list of strings")
    status = item.get("status")
    if status is not None and status not in STATUSES:
        errors.append(f"{model_id}: invalid status {status}")
    if role == "embedder" and item.get("embedding_dims") in (None, "late-interaction"):
        errors.append(f"{model_id}: dense embedders should declare integer or unknown dimensions")
    if role == "retriever" and item.get("embedding_dims") not in ("late-interaction", "unknown", None):
        errors.append(f"{model_id}: retrievers should not pretend to be a plain dense collection unless proven")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-hf", action="store_true", help="Query Hugging Face for candidate repo metadata")
    args = parser.parse_args()

    data = yaml.safe_load(RADAR.read_text(encoding="utf-8"))
    candidates = data.get("candidates", [])
    if not isinstance(candidates, list):
        raise ValueError(f"{RADAR}: candidates must be a list")

    failed = False
    api = HfApi() if args.check_hf else None
    for item in candidates:
        if not isinstance(item, dict):
            print("schema: candidate entry is not an object")
            failed = True
            continue
        errors = validate_candidate(item)
        for error in errors:
            print(f"schema: {error}")
        failed = failed or bool(errors)

        model_id = str(item.get("id", ""))
        print(f"\n== {model_id}")
        print(f"role: {item.get('role')}")
        print(f"status: {item.get('status')}")
        print(f"first_gate: {item.get('first_gate')}")
        if args.check_hf and api is not None and is_hf_repo(model_id):
            try:
                info = api.model_info(model_id)
            except Exception as exc:  # noqa: BLE001
                print(f"huggingface: missing/error: {type(exc).__name__}: {str(exc).splitlines()[0]}")
                failed = True
                continue
            tags = ",".join((info.tags or [])[:12])
            print("huggingface: exists")
            print(f"private: {info.private}")
            print(f"modified: {info.lastModified}")
            print(f"downloads: {info.downloads}")
            print(f"likes: {info.likes}")
            print(f"tags: {tags}")
        elif args.check_hf:
            print("huggingface: skipped non-HF or Ollama-style id")

    collections = data.get("collections", [])
    if not isinstance(collections, list):
        print("schema: collections must be a list")
        failed = True
    for collection in collections:
        if not isinstance(collection, dict) or not collection.get("name"):
            print("schema: collection entry missing name")
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
