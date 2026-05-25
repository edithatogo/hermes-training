# mem0 Run Card

Date: 2026-05-25T17:20:06.172294+00:00
Run ID: mem0-fixture-qwen3-06b-recency-20260526
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-fixture-qwen3-06b-recency-20260526/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | memory+rerank |
| Model/tool | `hermes_fixture` |
| Runtime | hermes_fixture |
| Endpoint | |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-fixture-qwen3-06b-recency-20260526` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool hermes_fixture \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --rerank-model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --qwen3-local-files-only \
  --qwen3-server-url http://127.0.0.1:8765 \
  --rerank-strategy qwen3_causal_lm \
  --recency-weight 0.2 \
  --run-id mem0-fixture-qwen3-06b-recency-20260526
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.400 |
| Rerank pass rate | 1.000 |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.400 |
| Recency conflict pass rate | 0.000 |
| Distractor resistance pass rate | 1.000 |
| JSON validity rate |  |
| Add latency p50 | 2.873 |
| Search/embed/extract latency p50 | 2.867 |
| Search/embed/extract latency p95 | 2.913 |
| Rerank latency p50 | 0.495 |

## Decision

Promote / keep testing / reject: keep testing

Reason: Inline reranking fixed this seed recency suite, but raw vector ranking still failed and the suite is too small for default promotion.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
