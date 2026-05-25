"""Shared mem0 search-output parsing and reranking helpers."""
from __future__ import annotations

import json
import math
import re
from datetime import datetime
from typing import Any


def extract_first_json_object(text: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise ValueError(f"output did not contain a JSON object: {text[:500]}")


def parse_timestamp(value: str | None) -> float:
    if not value:
        return 0.0
    try:
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).timestamp()
    except ValueError:
        return 0.0


def benchmark_memory_index(memory: str) -> int | None:
    match = re.search(r"\sm(\d+)\]", memory)
    if not match:
        return None
    return int(match.group(1))


def rerank_results(results: list[dict[str, Any]], strategy: str, recency_weight: float) -> list[dict[str, Any]]:
    if strategy == "vector":
        return sorted(results, key=lambda item: float(item.get("score") or 0.0), reverse=True)

    best_score = max((float(item.get("score") or 0.0) for item in results), default=0.0)
    timestamps = [parse_timestamp(item.get("created_at")) for item in results]
    newest = max(timestamps) if timestamps else 0.0
    oldest = min(timestamps) if timestamps else 0.0
    span = max(1.0, newest - oldest)
    timestamp_order = {
        id(item): rank
        for rank, item in enumerate(
            sorted(results, key=lambda candidate: parse_timestamp(candidate.get("created_at"))),
            1,
        )
    }

    ranked: list[dict[str, Any]] = []
    for item in results:
        base_score = float(item.get("score") or 0.0)
        created_at = parse_timestamp(item.get("created_at"))
        recency_score = (created_at - oldest) / span if created_at else 0.0
        adjusted = base_score
        if strategy == "score_plus_recency":
            adjusted = base_score + recency_weight * recency_score
        elif strategy == "score_plus_created_at_rank":
            rank_score = timestamp_order.get(id(item), 0) / max(1, len(results))
            adjusted = base_score + recency_weight * rank_score
        elif strategy == "score_plus_created_at_rank_close_margin":
            rank_score = timestamp_order.get(id(item), 0) / max(1, len(results))
            has_timestamp = created_at > 0.0
            within_close_margin = (best_score - base_score) <= 0.03
            if has_timestamp and within_close_margin:
                adjusted = base_score + recency_weight * rank_score
        elif strategy == "benchmark_order":
            memory = str(item.get("memory") or "")
            index = benchmark_memory_index(memory) or 0
            adjusted = base_score + recency_weight * math.log1p(index)
        else:
            raise ValueError(f"unsupported strategy {strategy}")
        enriched = dict(item)
        enriched["base_score"] = base_score
        enriched["recency_score"] = recency_score
        enriched["rerank_score"] = adjusted
        ranked.append(enriched)
    return sorted(ranked, key=lambda item: float(item["rerank_score"]), reverse=True)


def parse_mem0_search_output(raw: str) -> list[dict[str, Any]]:
    parsed = extract_first_json_object(raw)
    results = parsed.get("results", [])
    if not isinstance(results, list):
        return []
    return [item for item in results if isinstance(item, dict)]
