# mem0 Run Card

Date: 2026-06-11T14:54:58.119670+00:00
Run ID: jina-mlx-text-matching-smoke-20260612c
Summary: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-smoke-20260612c/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | embedder |
| Model/tool | `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` |
| Runtime | mlx-native |
| Endpoint | |
| Collection or index | |
| Embedding dims | 1024 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-smoke-20260612c` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_jina_mlx_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v5-omni-small-text-matching-mlx \
  --task-type text-matching \
  --suite /Volumes/PortableSSD/GitHub/hermes-training/benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id jina-mlx-text-matching-smoke-20260612c
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 1.000 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 1.000 |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 0.022 |
| Search/embed/extract latency p95 | 0.118 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The endpoint path is proven, but the embedding model still needs a recency or reranking fix before promotion beyond the current default.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
