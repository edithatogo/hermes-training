#!/usr/bin/env python3
"""Run an embedding retrieval benchmark with sentence-transformers."""
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
        missing = {"id", "query", "documents"} - set(case)
        if missing:
            raise ValueError(f"{suite_path}:{index}: missing keys {sorted(missing)}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{suite_path}:{index}: id must be non-empty")
        if case_id in seen_ids:
            raise ValueError(f"{suite_path}: duplicate case id {case_id}")
        seen_ids.add(case_id)
        docs = case["documents"]
        if not isinstance(case.get("query"), str) or not case["query"]:
            raise ValueError(f"{case_id}: query must be non-empty")
        if not isinstance(docs, list) or len(docs) < 2:
            raise ValueError(f"{case_id}: documents must contain at least two items")
        if not any(bool(doc.get("relevant")) for doc in docs if isinstance(doc, dict)):
            raise ValueError(f"{case_id}: at least one document must be relevant")
        for doc in docs:
            if not isinstance(doc, dict):
                raise ValueError(f"{case_id}: document must be an object")
            if not isinstance(doc.get("id"), str) or not doc["id"]:
                raise ValueError(f"{case_id}: document id must be non-empty")
            if not isinstance(doc.get("text"), str) or not doc["text"]:
                raise ValueError(f"{case_id}: document text must be non-empty")


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


def load_model(model_id: str, device: str | None) -> Any:
    try:
        from sentence_transformers import SentenceTransformer
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "sentence-transformers is not installed. Install optional deps with "
            "`python -m pip install -r requirements-mem0-embeddings.txt`."
        ) from exc
    kwargs: dict[str, Any] = {}
    if device:
        kwargs["device"] = device
    return SentenceTransformer(model_id, **kwargs)


def encode(model: Any, text: str, normalize: bool) -> tuple[list[float], float]:
    started = time.time()
    vector = model.encode(text, normalize_embeddings=normalize)
    latency_s = time.time() - started
    if hasattr(vector, "tolist"):
        vector = vector.tolist()
    if not isinstance(vector, list) or not vector:
        raise ValueError("model returned an empty or unsupported embedding")
    return [float(value) for value in vector], latency_s


def cosine(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError(f"embedding dimension mismatch: {len(left)} != {len(right)}")
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def reciprocal_rank(ranked_docs: list[dict[str, Any]]) -> float:
    for index, doc in enumerate(ranked_docs, 1):
        if doc["relevant"]:
            return 1.0 / index
    return 0.0


def ndcg_at_k(ranked_docs: list[dict[str, Any]], k: int) -> float:
    gains = [1.0 if doc["relevant"] else 0.0 for doc in ranked_docs[:k]]
    dcg = sum(gain / math.log2(index + 2) for index, gain in enumerate(gains))
    ideal_count = min(k, sum(1 for doc in ranked_docs if doc["relevant"]))
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
        f"# sentence-transformers Embedding Benchmark: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Model: `{summary['model']}`",
        f"Device: `{summary['device']}`",
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
        f"| Embedding dims | {summary['embedding_dims']} |",
        f"| Embed latency p50 | {summary['embed_latency_p50_s']:.3f}s |",
        f"| Embed latency p95 | {summary['embed_latency_p95_s']:.3f}s |",
        "",
        "## Cases",
        "",
        "| Case | Top document | Pass |",
        "|---|---|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['id']} | {row['top_doc_id']} | {row['top1_pass']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=Path(__file__).resolve().parents[1] / "benchmarks" / "embeddings" / "memory_retrieval_suite.json")
    parser.add_argument("--model", default="BAAI/bge-m3")
    parser.add_argument("--device", help="Optional sentence-transformers device, for example cpu or mps.")
    parser.add_argument("--no-normalize", action="store_true")
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = load_json(args.suite)
    if not isinstance(suite, list):
        raise ValueError(f"{args.suite}: expected JSON array")
    validate_suite(suite, args.suite)

    run_id = args.run_id or f"sentence-transformers-embedding-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (resolve_default_output_root() / "embedding-benchmark" / run_id)

    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"model: {args.model}")
        print(f"device: {args.device or 'auto'}")
        print(f"normalize: {not args.no_normalize}")
        print(f"output_dir: {output_dir}")
        return 0

    model = load_model(args.model, args.device)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    latencies: list[float] = []
    embedding_dims = 0

    for index, case in enumerate(suite, 1):
        print(f"  [{index}/{len(suite)}] {case['id']}")
        query_embedding, latency_s = encode(model, case["query"], not args.no_normalize)
        latencies.append(latency_s)
        embedding_dims = len(query_embedding)

        ranked: list[dict[str, Any]] = []
        for doc in case["documents"]:
            doc_embedding, doc_latency_s = encode(model, doc["text"], not args.no_normalize)
            latencies.append(doc_latency_s)
            ranked.append(
                {
                    "id": doc["id"],
                    "text": doc["text"],
                    "relevant": bool(doc.get("relevant")),
                    "score": cosine(query_embedding, doc_embedding),
                }
            )
        ranked.sort(key=lambda item: item["score"], reverse=True)
        rows.append(
            {
                "id": case["id"],
                "query": case["query"],
                "top_doc_id": ranked[0]["id"],
                "top1_pass": ranked[0]["relevant"],
                "reciprocal_rank": reciprocal_rank(ranked),
                "ndcg_at_3": ndcg_at_k(ranked, 3),
                "recall_at_3": 1.0 if any(doc["relevant"] for doc in ranked[:3]) else 0.0,
                "ranked_docs": [
                    {"id": doc["id"], "relevant": doc["relevant"], "score": round(doc["score"], 6)}
                    for doc in ranked
                ],
            }
        )

    cases = len(rows)
    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "output_dir": str(output_dir),
        "model": args.model,
        "device": args.device or "auto",
        "endpoint_kind": "sentence-transformers",
        "normalize_embeddings": not args.no_normalize,
        "cases": cases,
        "top1_accuracy": sum(1 for row in rows if row["top1_pass"]) / max(1, cases),
        "recall_at_3": statistics.fmean(row["recall_at_3"] for row in rows),
        "mrr": statistics.fmean(row["reciprocal_rank"] for row in rows),
        "ndcg_at_3": statistics.fmean(row["ndcg_at_3"] for row in rows),
        "embedding_dims": embedding_dims,
        "embed_latency_mean_s": statistics.fmean(latencies) if latencies else 0.0,
        "embed_latency_p50_s": percentile(latencies, 0.50),
        "embed_latency_p95_s": percentile(latencies, 0.95),
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
