# mem0 Run Card

Date: 2026-06-12T14:21:06.387471+00:00
Run ID: jina-mlx-text-matching-differentiation-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-differentiation-20260613/summary.json`

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
| Output | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-differentiation-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_jina_mlx_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v5-omni-small-text-matching-mlx \
  --task-type text-matching \
  --repo-dir /Volumes/PortableSSD/huggingface/hub/jina-mlx/jina-mlx-text-matching-smoke-20260612b \
  --local-files-only \
  --suite benchmarks/embeddings/memory_retrieval_differentiation_suite.json \
  --run-id jina-mlx-text-matching-differentiation-20260613
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.700 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 0.900 |
| Top-1 expected rate | 0.700 |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 0.025 |
| Search/embed/extract latency p95 | 0.029 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The endpoint path is proven, but the embedding model still needs a recency or reranking fix before promotion beyond the current default.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
