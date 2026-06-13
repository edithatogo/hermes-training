#!/usr/bin/env python3
"""Replay rerank strategies over a copied live-store mem0 replay."""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from mem0_rerank_lib import rerank_results
except ModuleNotFoundError:
    from scripts.mem0_rerank_lib import rerank_results


DEFAULT_STRATEGIES = (
    "vector",
    "query_terms_guarded",
    "score_plus_created_at_rank",
    "score_plus_created_at_rank_close_margin",
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            payload = json.loads(line)
            if isinstance(payload, dict):
                rows.append(payload)
    return rows


def short_hash(value: str) -> str:
    return value[:12]


def result_hash(row: dict[str, Any]) -> str:
    value = row.get("hash")
    if isinstance(value, str) and value:
        return value
    source_hash = row.get("source_hash")
    if isinstance(source_hash, str) and source_hash:
        return source_hash
    raw = row.get("raw")
    if isinstance(raw, dict):
        metadata = raw.get("metadata")
        if isinstance(metadata, dict):
            source_hash = metadata.get("source_hash")
            if isinstance(source_hash, str) and source_hash:
                return source_hash
    return ""


def raw_result(row: dict[str, Any]) -> dict[str, Any]:
    raw = row.get("raw")
    if not isinstance(raw, dict):
        return {}
    enriched = dict(raw)
    enriched["query"] = str(row.get("query") or "")
    enriched["source_hash"] = result_hash(row)
    return enriched


def rows_by_query(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        query_id = str(row.get("query_id") or "")
        if query_id:
            grouped.setdefault(query_id, []).append(row)
    for grouped_rows in grouped.values():
        grouped_rows.sort(key=lambda item: int(item.get("rank") or 0))
    return grouped


def evaluate_strategy(
    strategy: str,
    default_by_query: dict[str, list[dict[str, Any]]],
    candidate_by_query: dict[str, list[dict[str, Any]]],
    recency_weight: float,
) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for query_id, default_rows in default_by_query.items():
        if not default_rows:
            continue
        candidate_rows = candidate_by_query.get(query_id, [])
        default_top = result_hash(default_rows[0])
        candidates = [raw_result(row) for row in candidate_rows]
        candidates = [item for item in candidates if item]
        ranked = rerank_results(candidates, strategy, recency_weight) if candidates else []
        ranked_hashes = [str(item.get("source_hash") or "") for item in ranked]
        candidate_top = ranked_hashes[0] if ranked_hashes else ""
        cases.append(
            {
                "query_id": query_id,
                "default_count": len(default_rows),
                "candidate_count": len(candidate_rows),
                "default_top_hash": default_top,
                "candidate_top_hash": candidate_top,
                "top1_match": bool(default_top and default_top == candidate_top),
                "default_top_recall_at_candidate_k": bool(default_top and default_top in ranked_hashes),
                "default_top_rank": ranked_hashes.index(default_top) + 1 if default_top in ranked_hashes else 0,
            }
        )
    comparable = [case for case in cases if case["default_count"] > 0]
    return {
        "strategy": strategy,
        "cases": cases,
        "metrics": {
            "comparable_cases": len(comparable),
            "top1_match_rate": sum(1 for case in comparable if case["top1_match"]) / max(1, len(comparable)),
            "default_top_recall_rate": sum(1 for case in comparable if case["default_top_recall_at_candidate_k"])
            / max(1, len(comparable)),
            "mean_default_top_rank": sum(float(case["default_top_rank"] or 0) for case in comparable)
            / max(1, len(comparable)),
        },
    }


def render_report(summary: dict[str, Any]) -> str:
    lines = [
        "# EmbeddingGemma Live-Store Rerank Replay",
        "",
        f"Run ID: `{summary['run_id']}`",
        f"Created: `{summary['created_at']}`",
        "",
        "## Scope",
        "",
        "This report replays local reranking strategies over the private copied",
        "live-store replay artifacts. Raw memory text is not committed; committed",
        "case rows use hashes only.",
        "",
        "## Strategy Metrics",
        "",
        "| Strategy | Comparable cases | Top-1 match | Default-top recall | Mean default-top rank | Decision |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for result in summary["strategy_results"]:
        metrics = result["metrics"]
        decision = "passes" if metrics["top1_match_rate"] == 1.0 else "does not pass"
        lines.append(
            "| {strategy} | {cases} | {top1:.3f} | {recall:.3f} | {rank:.3f} | {decision} |".format(
                strategy=f"`{result['strategy']}`",
                cases=metrics["comparable_cases"],
                top1=metrics["top1_match_rate"],
                recall=metrics["default_top_recall_rate"],
                rank=metrics["mean_default_top_rank"],
                decision=decision,
            )
        )
    lines.extend(
        [
            "",
            "## Best Strategy Cases",
            "",
            f"Best strategy: `{summary['best_strategy']}`",
            "",
            "| Query ID | Default count | Candidate count | Top-1 match | Recall | Default top rank | Default top hash | Candidate top hash |",
            "|---|---:|---:|---|---|---:|---|---|",
        ]
    )
    for case in summary["best_cases"]:
        lines.append(
            "| {query_id} | {default_count} | {candidate_count} | {top1} | {recall} | {rank} | `{default_hash}` | `{candidate_hash}` |".format(
                query_id=case["query_id"],
                default_count=case["default_count"],
                candidate_count=case["candidate_count"],
                top1="yes" if case["top1_match"] else "no",
                recall="yes" if case["default_top_recall_at_candidate_k"] else "no",
                rank=case["default_top_rank"],
                default_hash=short_hash(str(case["default_top_hash"])),
                candidate_hash=short_hash(str(case["candidate_top_hash"])),
            )
        )
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- Private default replay JSONL: `{summary['default_results_path']}`",
            f"- Private candidate replay JSONL: `{summary['candidate_results_path']}`",
            f"- Private redacted summary JSON: `{summary['summary_json_path']}`",
            "",
            "## Decision",
            "",
            summary["decision"],
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=f"embeddinggemma-live-store-rerank-replay-{datetime.now(UTC):%Y%m%d-%H%M%S}")
    parser.add_argument(
        "--source-run-dir",
        type=Path,
        default=Path("/Volumes/PortableSSD/hermes-evals/mem0-live-store-replay/embeddinggemma-live-store-replay-20260613"),
    )
    parser.add_argument("--strategy", action="append", choices=DEFAULT_STRATEGIES, default=[])
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("/Volumes/PortableSSD/hermes-evals/mem0-live-store-rerank-replay"),
    )
    parser.add_argument("--report-output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    default_results_path = args.source_run_dir / "private-default-search-results.jsonl"
    candidate_results_path = args.source_run_dir / "private-candidate-search-results.jsonl"
    default_rows = load_jsonl(default_results_path)
    candidate_rows = load_jsonl(candidate_results_path)
    default_by_query = rows_by_query(default_rows)
    candidate_by_query = rows_by_query(candidate_rows)
    strategies = args.strategy or list(DEFAULT_STRATEGIES)
    strategy_results = [
        evaluate_strategy(strategy, default_by_query, candidate_by_query, args.recency_weight) for strategy in strategies
    ]
    best = max(
        strategy_results,
        key=lambda result: (
            result["metrics"]["top1_match_rate"],
            result["metrics"]["default_top_recall_rate"],
            -result["metrics"]["mean_default_top_rank"],
        ),
    )
    decision = (
        f"`{best['strategy']}` fully restores default top-1 order on the copied-live-store replay."
        if best["metrics"]["top1_match_rate"] == 1.0
        else "No existing rerank strategy fully restores default top-1 order; keep EmbeddingGemma opt-in and non-default."
    )
    output_dir = args.output_root / args.run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "summary-redacted.json"
    summary = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "default_results_path": str(default_results_path),
        "candidate_results_path": str(candidate_results_path),
        "summary_json_path": str(summary_path),
        "strategies": strategies,
        "recency_weight": args.recency_weight,
        "query_count": len(default_by_query),
        "strategy_results": strategy_results,
        "best_strategy": best["strategy"],
        "best_cases": best["cases"],
        "decision": decision,
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path = args.report_output or output_dir / "report-redacted.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(summary), encoding="utf-8")
    print(json.dumps({"status": "passed", "summary": str(summary_path), "report": str(report_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
