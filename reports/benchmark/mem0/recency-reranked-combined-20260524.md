# mem0 Recency Suite With Inline Reranking

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool cmd \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --rerank-strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id mem0-current-nomic-recency-reranked-20260524
```

## Result

| Metric | Raw | Reranked |
|---|---:|---:|
| Cases | 5 | 5 |
| Pass rate | 0.400 | 1.000 |
| Top-1 expected rate | 0.400 | 1.000 |
| Recency conflict pass rate | 0.000 | 1.000 |
| Distractor resistance pass rate | 1.000 | 1.000 |
| Recall@k | 1.000 | n/a |

Latency and cleanup:

| Metric | Value |
|---|---:|
| Add latency p50 | 5.867s |
| Search latency p50 | 3.872s |
| Search latency p95 | 16.182s |
| Cleanup successes | 11 / 11 |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-reranked-20260524/results.jsonl`
- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-reranked-20260524/summary.md`

## Decision

This is now the preferred local command for comparing raw mem0 search ordering against the current heuristic reranker in one run.

The result confirms the earlier offline replay: current `nomic-embed-text` retrieval gets the right memory into the candidate set, but top-1 ranking is weak for updated facts. The `score_plus_created_at_rank` heuristic fixes the seed suite without changing the live mem0 config.

Do not promote the heuristic as the default until the suite is larger and includes more old-but-authoritative facts.
