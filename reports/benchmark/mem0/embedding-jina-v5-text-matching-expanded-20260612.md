# Jina v5 Text-Matching MLX Expanded Retrieval - 2026-06-12

## Scope

This run benchmarks `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx`
on the 12-case expanded mem0 retrieval suite from cached SSD MLX artifacts.

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
| Cases | 12 |
| Top-1 accuracy | 1.000 |
| Recall@3 | 1.000 |
| MRR | 1.000 |
| nDCG@3 | 1.000 |
| Embedding dims | 1024 |
| Embedding latency p50 | 0.019s |
| Embedding latency p95 | 0.020s |

Raw output:
`/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-expanded-20260612`

## Decision

Keep as benchmarked-not-promoted evidence. The expanded retrieval gate now
passes, but default mem0 promotion still requires a deliberate
`mem0_jina_v5_omni_small_1024` collection migration plus live add/search and
rollback proof back to `mem0_nomic_768`.
