# mem0 Recency Suite

Date: 2026-05-24

## Baseline Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool cmd \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --run-id mem0-current-nomic-recency-20260524
```

## Baseline Result

| Metric | Score |
|---|---:|
| Cases | 5 |
| Pass rate | 0.400 |
| Recall@k | 1.000 |
| Top-1 expected rate | 0.400 |
| Recency conflict pass rate | 0.000 |
| Distractor resistance pass rate | 1.000 |
| Add latency p50 | 2.905s |
| Search latency p50 | 2.890s |
| Search latency p95 | 3.798s |
| Cleanup successes | 11 / 11 |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-20260524/results.jsonl`
- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-20260524/summary.md`

## Rerank Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/evaluate_mem0_reranking.py \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --run-dir /Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-20260524 \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id recency-suite-created-at-rank-020-20260524
```

## Rerank Result

| Metric | Score |
|---|---:|
| Cases | 5 |
| Pass rate | 1.000 |
| Top-1 expected rate | 1.000 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 1.000 |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-20260524/rerank/recency-suite-created-at-rank-020-20260524/results.jsonl`
- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-20260524/rerank/recency-suite-created-at-rank-020-20260524/summary.md`

## Decision

The current mem0 retrieval path has high recall but weak top-1 ordering for updated facts. In this suite, the right memory is present in every result set, but the older conflicting memory often ranks first.

The `score_plus_created_at_rank` heuristic with weight `0.20` fixes all five seed cases without breaking direct recall or distractor resistance. Keep it as a prototype baseline and compare future candidates against it before changing live mem0 behavior.

Next candidates:

1. A safer conflict-aware recency scorer that only boosts memories in the same semantic/update cluster.
2. `Qwen/Qwen3-Reranker-4B` on the same saved candidate sets.
3. `BAAI/bge-m3` in a separate `mem0_bge_m3_1024` collection.
