# mem0 Reranking

Reranking sits between vector search and the final memories shown to an agent.

The current `nomic-embed-text` baseline retrieves the relevant current preference in the recency case, but ranks the older conflicting preference first. That means the first fix does not need to replace embeddings immediately; a post-ranker can be tested independently.

## Current Prototype

Offline evaluator:

```bash
source scripts/env.sh
./.venv/bin/python scripts/evaluate_mem0_reranking.py \
  --run-dir /Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524 \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id created-at-rank-020-20260524
```

Result on the first seed suite: `1.000` pass rate.

This is not enough to change live mem0 behavior. It proves the failure is addressable after retrieval. The next step is to expand the suite and compare:

- vector-only ordering
- `score_plus_created_at_rank`
- a learned/local reranker such as `Qwen/Qwen3-Reranker-4B`
- conflict-aware memory update/supersession metadata

## Integration Rule

A reranker must not hide relevant older facts just because they are old. Recency should help with preference updates and conflicts, but source-grounded facts still need semantic relevance to dominate.

