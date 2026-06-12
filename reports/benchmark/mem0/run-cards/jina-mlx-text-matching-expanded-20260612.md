# mem0 Run Card

Date: 2026-06-12T13:54:18.306661+00:00
Run ID: jina-mlx-text-matching-expanded-20260612
Summary: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-expanded-20260612/summary.json`

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
| Output | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-expanded-20260612` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_jina_mlx_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v5-omni-small-text-matching-mlx \
  --task-type text-matching \
  --repo-dir /Volumes/PortableSSD/huggingface/hub/jina-mlx/jina-mlx-text-matching-smoke-20260612b \
  --local-files-only \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --run-id jina-mlx-text-matching-expanded-20260612
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
| Search/embed/extract latency p50 | 0.019 |
| Search/embed/extract latency p95 | 0.020 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The embedding benchmark passed the expanded suite, but default promotion still needs a deliberate 1024-dim collection migration plan plus live mem0 add/search rollback proof.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
