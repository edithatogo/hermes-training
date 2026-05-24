#!/usr/bin/env python3
"""Evaluate reranking strategies on fixed query/candidate sets."""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from mem0_rerank_lib import rerank_results
except ModuleNotFoundError:
    from scripts.mem0_rerank_lib import rerank_results


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
    seen_ids: set[str] = set()
    for index, case in enumerate(suite, 1):
        if not isinstance(case, dict):
            raise ValueError(f"{suite_path}:{index}: case must be an object")
        missing = {"id", "category", "query", "candidates"} - set(case)
        if missing:
            raise ValueError(f"{suite_path}:{index}: missing keys {sorted(missing)}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{suite_path}:{index}: id must be non-empty")
        if case_id in seen_ids:
            raise ValueError(f"{suite_path}: duplicate case id {case_id}")
        seen_ids.add(case_id)
        if not isinstance(case["query"], str) or not case["query"]:
            raise ValueError(f"{case_id}: query must be non-empty")
        candidates = case["candidates"]
        if not isinstance(candidates, list) or len(candidates) < 2:
            raise ValueError(f"{case_id}: candidates must contain at least two items")
        if not any(isinstance(item, dict) and item.get("relevant") for item in candidates):
            raise ValueError(f"{case_id}: at least one candidate must be relevant")
        candidate_ids: set[str] = set()
        for candidate in candidates:
            if not isinstance(candidate, dict):
                raise ValueError(f"{case_id}: candidate must be an object")
            if not isinstance(candidate.get("id"), str) or not candidate["id"]:
                raise ValueError(f"{case_id}: candidate id must be non-empty")
            if candidate["id"] in candidate_ids:
                raise ValueError(f"{case_id}: duplicate candidate id {candidate['id']}")
            candidate_ids.add(candidate["id"])
            if not isinstance(candidate.get("text"), str) or not candidate["text"]:
                raise ValueError(f"{case_id}: candidate text must be non-empty")


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


def tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2}


def lexical_rerank(query: str, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    query_tokens = tokenize(query)
    ranked: list[dict[str, Any]] = []
    for item in candidates:
        candidate_tokens = tokenize(str(item.get("text") or item.get("memory") or ""))
        overlap = len(query_tokens & candidate_tokens)
        union = len(query_tokens | candidate_tokens) or 1
        enriched = dict(item)
        enriched["base_score"] = float(item.get("score") or 0.0)
        enriched["rerank_score"] = overlap / union
        ranked.append(enriched)
    return sorted(ranked, key=lambda item: float(item["rerank_score"]), reverse=True)


def cross_encoder_rerank(model_name: str, query: str, candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], float]:
    try:
        from sentence_transformers import CrossEncoder
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "sentence-transformers is not installed. Install optional deps with "
            "`python -m pip install -r requirements-mem0-rerankers.txt` or a compatible CrossEncoder stack."
        ) from exc

    started = time.time()
    model = CrossEncoder(model_name)
    load_latency_s = time.time() - started
    pairs = [(query, str(item.get("text") or item.get("memory") or "")) for item in candidates]
    scores = model.predict(pairs)
    if hasattr(scores, "tolist"):
        scores = scores.tolist()
    ranked: list[dict[str, Any]] = []
    for item, score in zip(candidates, scores, strict=True):
        enriched = dict(item)
        enriched["base_score"] = float(item.get("score") or 0.0)
        enriched["rerank_score"] = float(score)
        ranked.append(enriched)
    return sorted(ranked, key=lambda item: float(item["rerank_score"]), reverse=True), load_latency_s


def reciprocal_rank(ranked: list[dict[str, Any]]) -> float:
    for index, item in enumerate(ranked, 1):
        if item["relevant"]:
            return 1.0 / index
    return 0.0


def ndcg_at_k(ranked: list[dict[str, Any]], k: int) -> float:
    gains = [1.0 if item["relevant"] else 0.0 for item in ranked[:k]]
    dcg = sum(gain / math.log2(index + 2) for index, gain in enumerate(gains))
    ideal_count = min(k, sum(1 for item in ranked if item["relevant"]))
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
        f"# Fixed Reranking Benchmark: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Strategy: `{summary['strategy']}`",
        f"Model: `{summary.get('model', '')}`",
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
        f"| Recency conflict pass rate | {summary['recency_conflict_pass_rate']:.3f} |",
        f"| Distractor resistance pass rate | {summary['distractor_resistance_pass_rate']:.3f} |",
        f"| Rerank latency p50 | {summary['rerank_latency_p50_s']:.3f}s |",
        "",
        "## Cases",
        "",
        "| Case | Category | Top candidate | Pass |",
        "|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['id']} | {row['category']} | {row['top_candidate_id']} | {row['top1_pass']} |")
    lines.append("")
    return "\n".join(lines)


def rerank_case(case: dict[str, Any], strategy: str, recency_weight: float, model: str | None) -> tuple[list[dict[str, Any]], float]:
    candidates = [
        {
            "id": item["id"],
            "memory": item["text"],
            "text": item["text"],
            "score": float(item.get("score") or 0.0),
            "created_at": item.get("created_at"),
            "relevant": bool(item.get("relevant")),
        }
        for item in case["candidates"]
    ]
    started = time.time()
    if strategy == "lexical_overlap":
        ranked = lexical_rerank(case["query"], candidates)
    elif strategy == "cross_encoder":
        if not model:
            raise ValueError("--model is required for cross_encoder strategy")
        return cross_encoder_rerank(model, case["query"], candidates)
    else:
        ranked = rerank_results(candidates, strategy, recency_weight)
    return ranked, time.time() - started


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=Path(__file__).resolve().parents[1] / "benchmarks" / "mem0_reranking" / "fixed_candidate_suite.json")
    parser.add_argument(
        "--strategy",
        choices=("vector", "score_plus_recency", "score_plus_created_at_rank", "benchmark_order", "lexical_overlap", "cross_encoder"),
        default="vector",
    )
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--model")
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = load_json(args.suite)
    if not isinstance(suite, list):
        raise ValueError(f"{args.suite}: expected JSON array")
    validate_suite(suite, args.suite)

    run_id = args.run_id or f"fixed-rerank-{args.strategy}-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (resolve_default_output_root() / "mem0-reranking-benchmark" / run_id)

    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"strategy: {args.strategy}")
        print(f"model: {args.model or ''}")
        print(f"output_dir: {output_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    latencies: list[float] = []
    for index, case in enumerate(suite, 1):
        print(f"  [{index}/{len(suite)}] {case['id']}")
        ranked, latency_s = rerank_case(case, args.strategy, args.recency_weight, args.model)
        latencies.append(latency_s)
        rows.append(
            {
                "id": case["id"],
                "category": case["category"],
                "query": case["query"],
                "top_candidate_id": ranked[0]["id"],
                "top1_pass": bool(ranked[0]["relevant"]),
                "reciprocal_rank": reciprocal_rank(ranked),
                "ndcg_at_3": ndcg_at_k(ranked, 3),
                "recall_at_3": 1.0 if any(item["relevant"] for item in ranked[:3]) else 0.0,
                "rerank_latency_s": round(latency_s, 6),
                "ranked_candidates": [
                    {
                        "id": item["id"],
                        "relevant": item["relevant"],
                        "base_score": round(float(item.get("base_score", item.get("score", 0.0)) or 0.0), 6),
                        "rerank_score": round(float(item.get("rerank_score", item.get("score", 0.0)) or 0.0), 6),
                    }
                    for item in ranked
                ],
            }
        )

    cases = len(rows)
    recency_rows = [row for row in rows if row["category"] == "recency_conflict"]
    distractor_rows = [row for row in rows if row["category"] == "distractor_resistance"]
    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "output_dir": str(output_dir),
        "strategy": args.strategy,
        "model": args.model or "",
        "recency_weight": args.recency_weight,
        "cases": cases,
        "top1_accuracy": sum(1 for row in rows if row["top1_pass"]) / max(1, cases),
        "recall_at_3": statistics.fmean(row["recall_at_3"] for row in rows),
        "mrr": statistics.fmean(row["reciprocal_rank"] for row in rows),
        "ndcg_at_3": statistics.fmean(row["ndcg_at_3"] for row in rows),
        "recency_conflict_pass_rate": sum(1 for row in recency_rows if row["top1_pass"]) / max(1, len(recency_rows)),
        "distractor_resistance_pass_rate": sum(1 for row in distractor_rows if row["top1_pass"]) / max(1, len(distractor_rows)),
        "rerank_latency_mean_s": statistics.fmean(latencies) if latencies else 0.0,
        "rerank_latency_p50_s": percentile(latencies, 0.50),
        "rerank_latency_p95_s": percentile(latencies, 0.95),
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
