# mem0 Reranking: Created-At Rank Prototype

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/evaluate_mem0_reranking.py \
  --run-dir /Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524 \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id created-at-rank-020-20260524
```

## Result

| Metric | Score |
|---|---:|
| Cases | 3 |
| Pass rate | 1.000 |
| Top-1 expected rate | 1.000 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 1.000 |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524/rerank/created-at-rank-020-20260524/results.jsonl`
- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524/rerank/created-at-rank-020-20260524/summary.md`

## Decision

The current failure is fixable after retrieval: adding a modest created-at rank boost over the saved mem0 search results flips the recency-conflict case without breaking direct recall or distractor resistance in the seed suite.

Do not wire this into live mem0 yet. The seed suite has only three cases. Expand recency and stale-fact tests first, then compare this heuristic against `Qwen/Qwen3-Reranker-4B` and stronger embedders.

