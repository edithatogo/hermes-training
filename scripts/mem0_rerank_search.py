#!/usr/bin/env python3
"""Run mem0 search and apply a local reranking strategy without changing mem0 config."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from mem0_rerank_lib import parse_mem0_search_output, rerank_results
    from run_fixed_reranking_benchmark import mlx_cross_encoder_rerank, qwen3_causal_lm_rerank
except ModuleNotFoundError:
    from scripts.mem0_rerank_lib import parse_mem0_search_output, rerank_results
    from scripts.run_fixed_reranking_benchmark import mlx_cross_encoder_rerank, qwen3_causal_lm_rerank


def cli_safe_text(text: str) -> str:
    """Avoid a mem0 CLI search quoting bug around ASCII apostrophes."""
    return text.replace("'", " ")


def run_mem0_search(tool: str, query: str, timeout_s: float) -> tuple[list[dict[str, Any]], str, float]:
    started = time.time()
    completed = subprocess.run(
        ["mem0", tool, "search", cli_safe_text(query)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
    )
    latency_s = time.time() - started
    if completed.returncode != 0:
        raise RuntimeError(f"mem0 {tool} search failed with {completed.returncode}:\n{completed.stdout}")
    return parse_mem0_search_output(completed.stdout), completed.stdout, latency_s


def rerank_search_results(
    query: str,
    results: list[dict[str, Any]],
    strategy: str,
    recency_weight: float,
    model: str | None,
    qwen3_device: str,
    qwen3_max_length: int,
    qwen3_instruction: str,
    qwen3_local_files_only: bool = False,
    qwen3_server_url: str | None = None,
    mlx_max_length: int = 8192,
    retriever_service_url: str | None = None,
    retriever_timeout_s: float = 120.0,
) -> tuple[list[dict[str, Any]], float]:
    if not results:
        return [], 0.0
    if strategy == "retriever_service":
        if not retriever_service_url:
            raise ValueError("--retriever-service-url is required for retriever_service")
        return retriever_service_rerank(retriever_service_url, query, results, retriever_timeout_s)
    if strategy == "qwen3_causal_lm":
        if not model:
            raise ValueError("--model is required for qwen3_causal_lm")
        if qwen3_server_url:
            return qwen3_server_rerank(
                qwen3_server_url,
                query,
                results,
                model,
                qwen3_device,
                qwen3_max_length,
                qwen3_instruction,
                qwen3_local_files_only,
            )
        return qwen3_causal_lm_rerank(
            model,
            query,
            results,
            qwen3_device,
            qwen3_max_length,
            qwen3_instruction,
            local_files_only=qwen3_local_files_only,
        )
    if strategy == "mlx_cross_encoder":
        if not model:
            raise ValueError("--model is required for mlx_cross_encoder")
        return mlx_cross_encoder_rerank(model, query, results, mlx_max_length)
    rerank_started = time.time()
    ranked = rerank_results(results, strategy, recency_weight)
    return ranked, time.time() - rerank_started


def memory_text(item: dict[str, Any]) -> str:
    for key in ("memory", "text", "content"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return json.dumps(item, ensure_ascii=False, sort_keys=True)


def memory_id(item: dict[str, Any], index: int) -> str:
    value = item.get("id") or item.get("memory_id")
    if isinstance(value, str) and value:
        return value
    return f"mem0-result-{index}"


def retriever_service_rerank(
    service_url: str,
    query: str,
    results: list[dict[str, Any]],
    timeout_s: float,
) -> tuple[list[dict[str, Any]], float]:
    documents = []
    by_doc_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(results, 1):
        doc_id = memory_id(item, index)
        document = {
            "doc_id": doc_id,
            "text": memory_text(item),
            "created_at": item.get("created_at", ""),
            "score": item.get("score"),
            "metadata": item.get("metadata", {}),
        }
        documents.append(document)
        by_doc_id[doc_id] = item
    payload = {"query": query, "top_k": len(documents), "documents": documents}
    started = time.time()
    request = Request(
        service_url.rstrip("/") + "/retrieve",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout_s) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"retriever service returned HTTP {exc.code}: {exc.read().decode('utf-8')}") from exc
    except URLError as exc:
        raise RuntimeError(f"retriever service unavailable: {exc.reason}") from exc
    ranked_results = response_payload.get("results")
    if not isinstance(ranked_results, list):
        raise RuntimeError("retriever service response missing results list")
    ranked: list[dict[str, Any]] = []
    seen: set[str] = set()
    for result in ranked_results:
        if not isinstance(result, dict):
            continue
        doc_id = str(result.get("doc_id") or result.get("id") or "")
        original = by_doc_id.get(doc_id)
        if original is None:
            continue
        seen.add(doc_id)
        enriched = dict(original)
        enriched["base_score"] = float(original.get("score") or 0.0)
        enriched["rerank_score"] = float(result.get("score") or 0.0)
        enriched["retriever_score"] = enriched["rerank_score"]
        enriched["retriever_doc_id"] = doc_id
        ranked.append(enriched)
    for doc_id, original in by_doc_id.items():
        if doc_id in seen:
            continue
        enriched = dict(original)
        enriched["base_score"] = float(original.get("score") or 0.0)
        enriched["rerank_score"] = float("-inf")
        enriched["retriever_doc_id"] = doc_id
        ranked.append(enriched)
    return ranked, time.time() - started


def qwen3_server_rerank(
    server_url: str,
    query: str,
    results: list[dict[str, Any]],
    model: str,
    qwen3_device: str,
    qwen3_max_length: int,
    qwen3_instruction: str,
    qwen3_local_files_only: bool,
) -> tuple[list[dict[str, Any]], float]:
    payload = {
        "query": query,
        "results": results,
        "model": model,
        "device": qwen3_device,
        "max_length": qwen3_max_length,
        "instruction": qwen3_instruction,
        "local_files_only": qwen3_local_files_only,
    }
    started = time.time()
    request = Request(
        server_url.rstrip("/") + "/rerank",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=120) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Qwen3 reranker service returned HTTP {exc.code}: {exc.read().decode('utf-8')}") from exc
    except URLError as exc:
        raise RuntimeError(f"Qwen3 reranker service unavailable: {exc.reason}") from exc
    ranked = response_payload.get("results")
    if not isinstance(ranked, list):
        raise RuntimeError("Qwen3 reranker service response missing results list")
    latency_s = float(response_payload.get("rerank_latency_s", time.time() - started))
    return ranked, latency_s


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--tool", default="cmd")
    parser.add_argument(
        "--strategy",
        choices=(
            "vector",
            "score_plus_recency",
            "score_plus_created_at_rank",
            "score_plus_created_at_rank_close_margin",
            "benchmark_order",
            "qwen3_causal_lm",
            "mlx_cross_encoder",
            "retriever_service",
        ),
        default="score_plus_created_at_rank",
    )
    parser.add_argument("--model", help="Reranker model id for learned strategies.")
    parser.add_argument("--qwen3-device", default="auto", help="Device for qwen3_causal_lm: auto, mps, or cpu.")
    parser.add_argument("--qwen3-max-length", type=int, default=8192)
    parser.add_argument(
        "--qwen3-local-files-only",
        action="store_true",
        help="Use only the local Hugging Face cache for qwen3_causal_lm model loading.",
    )
    parser.add_argument("--qwen3-server-url", help="Warm local Qwen3 reranker service URL.")
    parser.add_argument("--mlx-max-length", type=int, default=8192)
    parser.add_argument("--retriever-service-url", default="http://127.0.0.1:8765")
    parser.add_argument("--retriever-timeout-s", type=float, default=120.0)
    parser.add_argument(
        "--qwen3-instruction",
        default="Retrieve memories that answer the query for a local Hermes agent.",
    )
    parser.add_argument("--recency-weight", type=float, default=0.20)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--include-raw", action="store_true")
    args = parser.parse_args()

    total_started = time.time()
    results, raw, search_latency_s = run_mem0_search(args.tool, args.query, args.timeout_s)
    try:
        ranked, rerank_latency_s = rerank_search_results(
            args.query,
            results,
            args.strategy,
            args.recency_weight,
            args.model,
            args.qwen3_device,
            args.qwen3_max_length,
            args.qwen3_instruction,
            args.qwen3_local_files_only,
            args.qwen3_server_url,
            args.mlx_max_length,
            args.retriever_service_url,
            args.retriever_timeout_s,
        )
    except (RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    total_latency_s = time.time() - total_started
    output = {
        "created_at": datetime.now(UTC).isoformat(),
        "tool": args.tool,
        "query": args.query,
        "strategy": args.strategy,
        "model": args.model or "",
        "recency_weight": args.recency_weight,
        "latency_s": round(search_latency_s, 3),
        "mem0_search_latency_s": round(search_latency_s, 3),
        "rerank_latency_s": round(rerank_latency_s, 3),
        "total_latency_s": round(total_latency_s, 3),
        "input_count": len(results),
        "results": ranked,
    }
    if args.strategy == "qwen3_causal_lm":
        output["qwen3_device"] = args.qwen3_device
        output["qwen3_max_length"] = args.qwen3_max_length
        output["qwen3_instruction"] = args.qwen3_instruction
        output["qwen3_local_files_only"] = args.qwen3_local_files_only
        output["qwen3_server_url"] = args.qwen3_server_url or ""
    if args.strategy == "mlx_cross_encoder":
        output["mlx_max_length"] = args.mlx_max_length
    if args.strategy == "retriever_service":
        output["retriever_service_url"] = args.retriever_service_url
    if args.include_raw:
        output["raw_mem0_output"] = raw
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
