#!/usr/bin/env python3
"""Replay multi-result mem0 reranking suites through the read-only wrapper path."""
from __future__ import annotations

import argparse
import json
import statistics
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from mem0_rerank_search import rerank_search_results
    from run_fixed_reranking_benchmark import (
        ndcg_at_k,
        percentile,
        reciprocal_rank,
        resolve_default_output_root,
        save_jsonl,
        validate_suite,
    )
except ModuleNotFoundError:
    from scripts.mem0_rerank_search import rerank_search_results
    from scripts.run_fixed_reranking_benchmark import (
        ndcg_at_k,
        percentile,
        reciprocal_rank,
        resolve_default_output_root,
        save_jsonl,
        validate_suite,
    )


def load_suite(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        suite = json.load(handle)
    if not isinstance(suite, list):
        raise ValueError(f"{path}: expected JSON array")
    validate_suite(suite, path)
    return suite


def suite_candidates_to_mem0_results(case: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for candidate in case["candidates"]:
        results.append(
            {
                "id": candidate["id"],
                "memory": candidate["text"],
                "text": candidate["text"],
                "score": float(candidate.get("score") or 0.0),
                "created_at": candidate.get("created_at"),
                "relevant": bool(candidate.get("relevant")),
            }
        )
    return results


def evaluate_case(
    case: dict[str, Any],
    strategy: str,
    recency_weight: float,
    model: str | None,
    qwen3_device: str,
    qwen3_max_length: int,
    qwen3_instruction: str,
    qwen3_local_files_only: bool,
    qwen3_server_url: str | None,
) -> dict[str, Any]:
    ranked, latency_s = rerank_search_results(
        case["query"],
        suite_candidates_to_mem0_results(case),
        strategy,
        recency_weight,
        model,
        qwen3_device,
        qwen3_max_length,
        qwen3_instruction,
        qwen3_local_files_only,
        qwen3_server_url,
    )
    return {
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
                "relevant": bool(item["relevant"]),
                "base_score": round(float(item.get("base_score", item.get("score", 0.0)) or 0.0), 6),
                "rerank_score": round(float(item.get("rerank_score", item.get("score", 0.0)) or 0.0), 6),
            }
            for item in ranked
        ],
    }


def summarize_rows(
    rows: list[dict[str, Any]],
    run_id: str,
    suite: Path,
    output_dir: Path,
    strategy: str,
    recency_weight: float,
    model: str | None,
    qwen3_device: str,
    qwen3_max_length: int,
    qwen3_instruction: str,
    qwen3_local_files_only: bool,
    qwen3_server_url: str | None,
) -> dict[str, Any]:
    cases = len(rows)
    recency_rows = [row for row in rows if row["category"] == "recency_conflict"]
    distractor_rows = [row for row in rows if row["category"] == "distractor_resistance"]
    latencies = [float(row["rerank_latency_s"]) for row in rows]
    return {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(suite),
        "output_dir": str(output_dir),
        "strategy": strategy,
        "model": model or "",
        "recency_weight": recency_weight,
        "qwen3_device": qwen3_device if strategy == "qwen3_causal_lm" else "",
        "qwen3_max_length": qwen3_max_length if strategy == "qwen3_causal_lm" else "",
        "qwen3_instruction": qwen3_instruction if strategy == "qwen3_causal_lm" else "",
        "qwen3_local_files_only": qwen3_local_files_only if strategy == "qwen3_causal_lm" else "",
        "qwen3_server_url": qwen3_server_url or "",
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


def render_summary_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# mem0 Rerank Replay: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Strategy: `{summary['strategy']}`",
        f"Model: `{summary.get('model', '')}`",
        f"Qwen3 service URL: `{summary.get('qwen3_server_url', '')}`",
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
        f"| Rerank latency p95 | {summary['rerank_latency_p95_s']:.3f}s |",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=Path(__file__).resolve().parents[1] / "benchmarks" / "mem0_reranking" / "fixed_candidate_suite.json")
    parser.add_argument(
        "--strategy",
        choices=(
            "vector",
            "score_plus_recency",
            "score_plus_created_at_rank",
            "score_plus_created_at_rank_close_margin",
            "benchmark_order",
            "qwen3_causal_lm",
        ),
        default="score_plus_created_at_rank_close_margin",
    )
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--model")
    parser.add_argument("--qwen3-device", default="auto")
    parser.add_argument("--qwen3-max-length", type=int, default=4096)
    parser.add_argument("--qwen3-instruction", default="Retrieve relevant memory")
    parser.add_argument("--qwen3-local-files-only", action="store_true")
    parser.add_argument("--qwen3-server-url")
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = load_suite(args.suite)
    run_id = args.run_id or f"mem0-rerank-replay-{args.strategy}-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (resolve_default_output_root() / "mem0-reranking-replay" / run_id)
    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"strategy: {args.strategy}")
        print(f"model: {args.model or ''}")
        print(f"qwen3_server_url: {args.qwen3_server_url or ''}")
        print(f"output_dir: {output_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        evaluate_case(
            case,
            args.strategy,
            args.recency_weight,
            args.model,
            args.qwen3_device,
            args.qwen3_max_length,
            args.qwen3_instruction,
            args.qwen3_local_files_only,
            args.qwen3_server_url,
        )
        for case in suite
    ]
    summary = summarize_rows(
        rows,
        run_id,
        args.suite,
        output_dir,
        args.strategy,
        args.recency_weight,
        args.model,
        args.qwen3_device,
        args.qwen3_max_length,
        args.qwen3_instruction,
        args.qwen3_local_files_only,
        args.qwen3_server_url,
    )
    save_jsonl(output_dir / "results.jsonl", rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_summary_markdown(summary, rows), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"results: {output_dir / 'results.jsonl'}")
    print(f"summary: {output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
