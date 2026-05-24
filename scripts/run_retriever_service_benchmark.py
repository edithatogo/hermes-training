#!/usr/bin/env python3
"""Benchmark a retriever service exposing POST /retrieve."""
from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def validate_suite(suite: list[Any], suite_path: Path) -> None:
    if not suite:
        raise ValueError(f"{suite_path}: empty suite")
    for index, case in enumerate(suite, 1):
        if not isinstance(case, dict):
            raise ValueError(f"{suite_path}:{index}: case must be an object")
        missing = {"id", "query", "documents"} - set(case)
        if missing:
            raise ValueError(f"{suite_path}:{index}: missing keys {sorted(missing)}")
        if not isinstance(case["query"], str) or not case["query"]:
            raise ValueError(f"{case.get('id', index)}: query must be non-empty")
        docs = case["documents"]
        if not isinstance(docs, list) or len(docs) < 2:
            raise ValueError(f"{case.get('id', index)}: documents must contain at least two items")
        if not any(isinstance(doc, dict) and doc.get("relevant") for doc in docs):
            raise ValueError(f"{case.get('id', index)}: at least one document must be relevant")


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


def retrieve(base_url: str, query: str, documents: list[dict[str, Any]], top_k: int, timeout_s: float) -> tuple[list[dict[str, Any]], float]:
    payload = {
        "query": query,
        "top_k": top_k,
        "documents": [
            {
                "doc_id": doc["id"],
                "text": doc["text"],
                "metadata": {key: value for key, value in doc.items() if key not in {"id", "text", "relevant"}},
            }
            for doc in documents
        ],
    }
    started = time.time()
    response = requests.post(base_url.rstrip("/") + "/retrieve", json=payload, timeout=timeout_s)
    latency_s = time.time() - started
    response.raise_for_status()
    data = response.json()
    results = data.get("results")
    if not isinstance(results, list):
        raise ValueError("retriever response missing results list")
    return [item for item in results if isinstance(item, dict)], latency_s


def reciprocal_rank(ranked_ids: list[str], relevant_ids: set[str]) -> float:
    for index, doc_id in enumerate(ranked_ids, 1):
        if doc_id in relevant_ids:
            return 1.0 / index
    return 0.0


def ndcg_at_k(ranked_ids: list[str], relevant_ids: set[str], k: int) -> float:
    gains = [1.0 if doc_id in relevant_ids else 0.0 for doc_id in ranked_ids[:k]]
    dcg = sum(gain / math.log2(index + 2) for index, gain in enumerate(gains))
    ideal_count = min(k, len(relevant_ids))
    ideal = sum(1.0 / math.log2(index + 2) for index in range(ideal_count))
    return dcg / ideal if ideal else 0.0


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    index = (len(ordered) - 1) * pct
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def render_summary_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# Retriever Service Benchmark: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Base URL: `{summary['base_url']}`",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Cases | {summary['cases']} |",
        f"| Top-1 accuracy | {summary['top1_accuracy']:.3f} |",
        f"| Recall@3 | {summary['recall_at_3']:.3f} |",
        f"| MRR | {summary['mrr']:.3f} |",
        f"| nDCG@3 | {summary['ndcg_at_3']:.3f} |",
        f"| Query latency p50 | {summary['query_latency_p50_s']:.3f}s |",
        f"| Query latency p95 | {summary['query_latency_p95_s']:.3f}s |",
        "",
        "## Cases",
        "",
        "| Case | Top doc | Pass |",
        "|---|---|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['id']} | {row['top_doc_id']} | {row['top1_pass']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=Path(__file__).resolve().parents[1] / "benchmarks" / "embeddings" / "memory_retrieval_suite.json")
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = load_json(args.suite)
    if not isinstance(suite, list):
        raise ValueError(f"{args.suite}: expected JSON array")
    validate_suite(suite, args.suite)

    run_id = args.run_id or f"retriever-service-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (resolve_default_output_root() / "mem0-retriever-benchmark" / run_id)

    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"base_url: {args.base_url}")
        print(f"top_k: {args.top_k}")
        print(f"output_dir: {output_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    latencies: list[float] = []
    for index, case in enumerate(suite, 1):
        print(f"  [{index}/{len(suite)}] {case['id']}")
        results, latency_s = retrieve(args.base_url, case["query"], case["documents"], args.top_k, args.timeout_s)
        latencies.append(latency_s)
        relevant_ids = {doc["id"] for doc in case["documents"] if doc.get("relevant")}
        ranked_ids = [str(item.get("doc_id") or item.get("id") or "") for item in results]
        rows.append(
            {
                "id": case["id"],
                "query": case["query"],
                "top_doc_id": ranked_ids[0] if ranked_ids else "",
                "top1_pass": bool(ranked_ids and ranked_ids[0] in relevant_ids),
                "recall_at_3": 1.0 if any(doc_id in relevant_ids for doc_id in ranked_ids[:3]) else 0.0,
                "reciprocal_rank": reciprocal_rank(ranked_ids, relevant_ids),
                "ndcg_at_3": ndcg_at_k(ranked_ids, relevant_ids, 3),
                "query_latency_s": round(latency_s, 6),
                "ranked_docs": ranked_ids,
            }
        )

    cases = len(rows)
    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "output_dir": str(output_dir),
        "base_url": args.base_url,
        "cases": cases,
        "top1_accuracy": sum(1 for row in rows if row["top1_pass"]) / max(1, cases),
        "recall_at_3": statistics.fmean(row["recall_at_3"] for row in rows),
        "mrr": statistics.fmean(row["reciprocal_rank"] for row in rows),
        "ndcg_at_3": statistics.fmean(row["ndcg_at_3"] for row in rows),
        "query_latency_mean_s": statistics.fmean(latencies) if latencies else 0.0,
        "query_latency_p50_s": percentile(latencies, 0.50),
        "query_latency_p95_s": percentile(latencies, 0.95),
    }
    save_jsonl(output_dir / "results.jsonl", rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_summary_markdown(summary, rows), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"results: {output_dir / 'results.jsonl'}")
    print(f"summary: {output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
