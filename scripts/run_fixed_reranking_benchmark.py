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

QWEN3_RERANKER_CACHE: dict[tuple[str, str, int, bool], tuple[Any, Any, int, int, str]] = {}
MLX_RERANKER_CACHE: dict[tuple[str, int], tuple[Any, Any, dict[str, Any]]] = {}


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


def xlm_roberta_pair_text(query: str, document: str) -> str:
    return f"<s>{query}</s></s>{document}</s>"


def load_mlx_reranker(model_name: str, max_length: int) -> tuple[Any, Any, dict[str, Any]]:
    cache_key = (model_name, max_length)
    if cache_key in MLX_RERANKER_CACHE:
        return MLX_RERANKER_CACHE[cache_key]
    try:
        from mlx_lm.utils import load
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "mlx-lm is required for mlx_cross_encoder reranking. "
            "Install the MLX runtime or use another reranking strategy."
        ) from exc

    model, tokenizer, config = load(model_name, return_config=True)
    model.eval()
    loaded = (model, tokenizer, config)
    MLX_RERANKER_CACHE[cache_key] = loaded
    return loaded


def mlx_cross_encoder_rerank(
    model_name: str,
    query: str,
    candidates: list[dict[str, Any]],
    max_length: int,
) -> tuple[list[dict[str, Any]], float]:
    try:
        import mlx.core as mx
    except ModuleNotFoundError as exc:
        raise SystemExit("mlx is required for mlx_cross_encoder reranking.") from exc

    started = time.time()
    model, tokenizer, config = load_mlx_reranker(model_name, max_length)
    load_and_score_started = time.time()
    pad_token_id = int(config.get("pad_token_id", 1))
    ranked: list[dict[str, Any]] = []
    for item in candidates:
        document = str(item.get("text") or item.get("memory") or "")
        ids = tokenizer.encode(xlm_roberta_pair_text(query, document))
        ids = ids[:max_length]
        input_ids = mx.array([ids], dtype=mx.int32)
        attention_mask = mx.where(input_ids != pad_token_id, 1, 0)
        logits = model(input_ids, attention_mask=attention_mask)
        mx.eval(logits)
        enriched = dict(item)
        enriched["base_score"] = float(item.get("score") or 0.0)
        enriched["rerank_score"] = float(mx.flatten(logits)[0].item())
        ranked.append(enriched)
    latency_s = time.time() - load_and_score_started if time.time() > started else 0.0
    return sorted(ranked, key=lambda item: float(item["rerank_score"]), reverse=True), latency_s


def qwen3_reranker_prompt(query: str, document: str, instruction: str) -> str:
    system_prompt = (
        "Judge whether the Document meets the requirements based on the Query and the Instruct provided. "
        'Note that the answer can only be "yes" or "no".'
    )
    return (
        f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        f"<|im_start|>user\n<Instruct>: {instruction}\n\n<Query>: {query}\n\n<Document>: {document}<|im_end|>\n"
        "<|im_start|>assistant\n<think>\n\n</think>\n"
    )


def load_qwen3_reranker(
    model_name: str,
    device: str,
    max_length: int,
    local_files_only: bool = False,
) -> tuple[Any, Any, int, int, str]:
    cache_key = (model_name, device, max_length, local_files_only)
    if cache_key in QWEN3_RERANKER_CACHE:
        return QWEN3_RERANKER_CACHE[cache_key]
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "transformers and torch are required for qwen3_causal_lm reranking. "
            "Install the base project dependencies or run a heuristic reranker instead."
        ) from exc

    resolved_device = device
    if device == "auto":
        resolved_device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float16 if resolved_device == "mps" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left", local_files_only=local_files_only)
    model = AutoModelForCausalLM.from_pretrained(model_name, dtype=dtype, local_files_only=local_files_only).to(resolved_device)
    model.eval()
    yes_id = tokenizer.convert_tokens_to_ids("yes")
    no_id = tokenizer.convert_tokens_to_ids("no")
    if yes_id is None or no_id is None or yes_id < 0 or no_id < 0:
        raise ValueError(f"{model_name}: tokenizer does not expose yes/no tokens")
    loaded = (tokenizer, model, int(yes_id), int(no_id), resolved_device)
    QWEN3_RERANKER_CACHE[cache_key] = loaded
    return loaded


def qwen3_causal_lm_rerank(
    model_name: str,
    query: str,
    candidates: list[dict[str, Any]],
    device: str,
    max_length: int,
    instruction: str,
    local_files_only: bool = False,
) -> tuple[list[dict[str, Any]], float]:
    try:
        import torch
    except ModuleNotFoundError as exc:
        raise SystemExit("torch is required for qwen3_causal_lm reranking.") from exc

    started = time.time()
    tokenizer, model, yes_id, no_id, resolved_device = load_qwen3_reranker(
        model_name,
        device,
        max_length,
        local_files_only=local_files_only,
    )
    load_and_score_started = time.time()
    ranked: list[dict[str, Any]] = []
    for item in candidates:
        document = str(item.get("text") or item.get("memory") or "")
        prompt = qwen3_reranker_prompt(query, document, instruction)
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_length)
        inputs = {key: value.to(resolved_device) for key, value in inputs.items()}
        with torch.inference_mode():
            output = model(**inputs)
        logits = output.logits[0, -1, [yes_id, no_id]]
        score = torch.softmax(logits.float(), dim=0)[0].item()
        enriched = dict(item)
        enriched["base_score"] = float(item.get("score") or 0.0)
        enriched["rerank_score"] = float(score)
        ranked.append(enriched)
    latency_s = time.time() - load_and_score_started if time.time() > started else 0.0
    return sorted(ranked, key=lambda item: float(item["rerank_score"]), reverse=True), latency_s


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


def rerank_case(
    case: dict[str, Any],
    strategy: str,
    recency_weight: float,
    model: str | None,
    qwen3_device: str = "auto",
    qwen3_max_length: int = 4096,
    qwen3_instruction: str = "Retrieve relevant memory",
    qwen3_local_files_only: bool = False,
    mlx_max_length: int = 8192,
) -> tuple[list[dict[str, Any]], float]:
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
    elif strategy == "qwen3_causal_lm":
        if not model:
            raise ValueError("--model is required for qwen3_causal_lm strategy")
        return qwen3_causal_lm_rerank(
            model,
            case["query"],
            candidates,
            device=qwen3_device,
            max_length=qwen3_max_length,
            instruction=qwen3_instruction,
            local_files_only=qwen3_local_files_only,
        )
    elif strategy == "mlx_cross_encoder":
        if not model:
            raise ValueError("--model is required for mlx_cross_encoder strategy")
        return mlx_cross_encoder_rerank(
            model,
            case["query"],
            candidates,
            max_length=mlx_max_length,
        )
    else:
        ranked = rerank_results(candidates, strategy, recency_weight)
    return ranked, time.time() - started


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
            "lexical_overlap",
            "cross_encoder",
            "mlx_cross_encoder",
            "qwen3_causal_lm",
        ),
        default="vector",
    )
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--model")
    parser.add_argument("--qwen3-device", default="auto", help="Device for qwen3_causal_lm: auto, mps, or cpu.")
    parser.add_argument("--qwen3-max-length", type=int, default=4096)
    parser.add_argument("--qwen3-instruction", default="Retrieve relevant memory")
    parser.add_argument("--qwen3-local-files-only", action="store_true")
    parser.add_argument("--mlx-max-length", type=int, default=8192)
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
        if args.strategy == "qwen3_causal_lm":
            print(f"qwen3_device: {args.qwen3_device}")
            print(f"qwen3_max_length: {args.qwen3_max_length}")
            print(f"qwen3_local_files_only: {args.qwen3_local_files_only}")
        if args.strategy == "mlx_cross_encoder":
            print(f"mlx_max_length: {args.mlx_max_length}")
        print(f"output_dir: {output_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    latencies: list[float] = []
    for index, case in enumerate(suite, 1):
        print(f"  [{index}/{len(suite)}] {case['id']}")
        ranked, latency_s = rerank_case(
            case,
            args.strategy,
            args.recency_weight,
            args.model,
            qwen3_device=args.qwen3_device,
            qwen3_max_length=args.qwen3_max_length,
            qwen3_instruction=args.qwen3_instruction,
            qwen3_local_files_only=args.qwen3_local_files_only,
            mlx_max_length=args.mlx_max_length,
        )
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
        "qwen3_device": args.qwen3_device if args.strategy == "qwen3_causal_lm" else "",
        "qwen3_max_length": args.qwen3_max_length if args.strategy == "qwen3_causal_lm" else "",
        "qwen3_instruction": args.qwen3_instruction if args.strategy == "qwen3_causal_lm" else "",
        "qwen3_local_files_only": args.qwen3_local_files_only if args.strategy == "qwen3_causal_lm" else "",
        "mlx_max_length": args.mlx_max_length if args.strategy == "mlx_cross_encoder" else "",
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
