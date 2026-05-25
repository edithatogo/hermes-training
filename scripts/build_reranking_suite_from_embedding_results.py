#!/usr/bin/env python3
"""Build a fixed reranking suite from embedding benchmark results."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def resolve_default_output_root() -> Path:
    env_eval_root = os.environ.get("HERMES_EVAL_ROOT")
    if env_eval_root:
        return Path(env_eval_root)
    storage_root = os.environ.get("HERMES_STORAGE_ROOT")
    if storage_root:
        return Path(storage_root) / "hermes-evals"
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD") / "hermes-evals"
    return Path.cwd() / ".local-storage" / "hermes-evals"


def build_suite(embedding_suite: list[dict[str, Any]], result_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cases_by_id = {case["id"]: case for case in embedding_suite}
    built: list[dict[str, Any]] = []
    for row in result_rows:
        case_id = row["id"]
        case = cases_by_id[case_id]
        docs_by_id = {doc["id"]: doc for doc in case["documents"]}
        candidates: list[dict[str, Any]] = []
        for ranked_doc in row["ranked_docs"]:
            doc = docs_by_id[ranked_doc["id"]]
            candidate = {
                "id": doc["id"],
                "text": doc["text"],
                "score": ranked_doc["score"],
                "relevant": bool(doc.get("relevant")),
            }
            if "created_at" in doc:
                candidate["created_at"] = doc["created_at"]
            candidates.append(candidate)
        built.append(
            {
                "id": case_id,
                "category": case.get("category", "embedding_retrieval"),
                "query": case["query"],
                "candidates": candidates,
            }
        )
    return built


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--run-id", default="embedding-derived-reranking-suite")
    args = parser.parse_args()

    embedding_suite = load_json(args.suite)
    result_rows = load_jsonl(args.results)
    if not isinstance(embedding_suite, list):
        raise ValueError(f"{args.suite}: expected JSON array")
    output = args.output or (
        resolve_default_output_root() / "mem0-reranking-benchmark" / args.run_id / "candidate-suite.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    built = build_suite(embedding_suite, result_rows)
    output.write_text(json.dumps(built, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output)
    print(f"cases: {len(built)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
