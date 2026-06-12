# Jina MLX Embedding Benchmark: jina-mlx-retrieval-expanded-20260613

Date: 2026-06-12T14:10:51.146940+00:00
Model: `jinaai/jina-embeddings-v5-omni-small-mlx`
Task: `retrieval`
Repo dir: `/Volumes/PortableSSD/huggingface/hub/jina-mlx/jina-mlx-retrieval-smoke-20260612b`
Raw output: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-retrieval-expanded-20260613`
Run card: `reports/benchmark/mem0/run-cards/jina-mlx-retrieval-expanded-20260613.md`

## Result

| Metric | Value |
|---|---:|
| Cases | 12 |
| Top-1 accuracy | 0.833 |
| Recall@3 | 1.000 |
| MRR | 0.917 |
| nDCG@3 | 0.938 |
| Embedding dims | 1024 |
| Embed latency mean | 0.022s |
| Embed latency p50 | 0.020s |
| Embed latency p95 | 0.022s |

## Cases

| Case | Top document | Pass |
|---|---|---:|
| metadata-database | target-sqlite | True |
| recency-preference | old-preference | False |
| benchmark-type | mem0-memory | True |
| artifact-path-direct | target-exports | True |
| extractor-preference-update | older-hermes | False |
| semantic-margin-beats-recency | target-collection | True |
| publication-gate | target-approval | True |
| adapter-promotion | target-v4 | True |
| azure-quota | target-quota | True |
| ollama-retest | target-after-upgrade | True |
| lfm25-guard | target-empty-response | True |
| storage-policy | target-evals | True |

## Misses

| Case | Expected | Top-1 | Note |
|---|---|---|---|
| recency-preference | `current-preference` | `old-preference` | Scores were close: 0.8349 vs 0.8358. |
| extractor-preference-update | `current-lfm2` | `older-hermes` | Scores were close: 0.7362 vs 0.7446. |

## Decision

Keep as benchmarked evidence, not a default mem0 embedder. It is fast and
recall-safe on the expanded suite, but the 0.833 top-1 result trails
`jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` at 1.000 and still
requires a 1024-dim collection migration plus live add/search rollback proof.

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
