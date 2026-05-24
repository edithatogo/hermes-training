# mem0 Run Card

Date: 2026-05-24T07:55:43.821689+00:00
Run ID: fixed-rerank-lexical-overlap-expanded-20260524
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-lexical-overlap-expanded-20260524/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | |
| Runtime | lexical_overlap |
| Endpoint | |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/fixed-rerank-lexical-overlap-expanded-20260524` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy lexical_overlap \
  --suite /Volumes/PortableSSD/GitHub/hermes-training/benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id fixed-rerank-lexical-overlap-expanded-20260524
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.833 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.833 |
| Recency conflict pass rate | 0.500 |
| Distractor resistance pass rate | 1.000 |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 |  |
| Search/embed/extract latency p95 |  |
| Rerank latency p50 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: This reranker did not reach the strict fixed-suite gate and should remain a comparison baseline.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
