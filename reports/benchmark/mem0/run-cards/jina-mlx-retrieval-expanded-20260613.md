# mem0 Run Card

Date: 2026-06-12T14:10:51.146940+00:00
Run ID: jina-mlx-retrieval-expanded-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-retrieval-expanded-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | embedder |
| Model/tool | `jinaai/jina-embeddings-v5-omni-small-mlx` |
| Runtime | mlx-native |
| Endpoint | |
| Collection or index | |
| Embedding dims | 1024 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-retrieval-expanded-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_jina_mlx_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v5-omni-small-mlx \
  --task-type retrieval \
  --repo-dir /Volumes/PortableSSD/huggingface/hub/jina-mlx/jina-mlx-retrieval-smoke-20260612b \
  --local-files-only \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --run-id jina-mlx-retrieval-expanded-20260613
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.833 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.833 |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 0.020 |
| Search/embed/extract latency p95 | 0.022 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The endpoint path is proven, but the embedding model still needs a recency or reranking fix before promotion beyond the current default.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
