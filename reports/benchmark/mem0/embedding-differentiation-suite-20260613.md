# mem0 Differentiation Benchmark - 2026-06-13

## Why This Exists

The earlier 3-case and 12-case retrieval suites are useful smoke and regression
gates, but several candidates were saturating them. This suite adds harder
near-duplicate operational-memory cases across version boundaries,
default-vs-candidate role boundaries, path scope, cloud backend priority,
cache completeness, runtime surface, and blocked-action decisions.

## New Suites

| Suite | Cases | Purpose |
|---|---:|---|
| `benchmarks/embeddings/memory_retrieval_differentiation_suite.json` | 10 | Isolated embedding retrieval with six close documents per query |
| `benchmarks/mem0_memory/live_fixture_differentiation_suite.json` | 8 | Real mem0 add/search fixture with four setup memories per query |

## Embedding Results

| Model | Runtime | Dims | Top-1 | Recall@3 | MRR | nDCG@3 | p50 embed |
|---|---|---:|---:|---:|---:|---:|---:|
| `BAAI/bge-m3` | sentence-transformers CPU | 1024 | 0.900 | 1.000 | 0.933 | 0.950 | 0.109s |
| `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | MLX cached local files | 1024 | 0.700 | 0.900 | 0.825 | 0.826 | 0.025s |
| `nomic-embed-text:latest` | Ollama | 768 | 0.600 | 0.800 | 0.750 | 0.726 | 0.019s |

## Miss Patterns

| Model | Missed top-1 cases |
|---|---|
| `BAAI/bge-m3` | `runtime-validation-boundary` |
| `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | `embedder-default-vs-best-score`, `storage-artifact-boundary`, `runtime-validation-boundary` |
| `nomic-embed-text:latest` | `dataset-publish-scope`, `storage-artifact-boundary`, `runtime-validation-boundary`, `azure-quota-no-compute` |

## Live mem0 Fixture Result

| Strategy | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | Distractor resistance |
|---|---:|---:|---:|---:|---:|---:|
| `vector` | 0.750 | 0.875 | 0.792 | 0.812 | 0.000 | 0.667 |
| `score_plus_created_at_rank_close_margin` | 0.750 | 0.875 | 0.792 | 0.812 | 0.000 | 0.667 |

The live fixture used an output-local `MEM0_CONFIG_PATH`, isolated Qdrant path,
and no default collection mutation. It shows the current guarded mem0 path
still struggles with some operational-boundary and recency cases, so further
promotion decisions should use this differentiation suite alongside the easier
expanded suite.

## Raw Evidence

| Run | Output |
|---|---|
| `embedding-bge-m3-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-differentiation-20260613` |
| `jina-mlx-text-matching-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-differentiation-20260613` |
| `embedding-nomic-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-differentiation-20260613` |
| `mem0-live-fixture-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-differentiation-20260613` |

## Decision

Use the differentiation suite for future mem0 embedder and reranker promotion
claims. The older expanded suite remains a regression gate, but it is no
longer sufficient on its own because it lets too many candidates converge on
similar scores.
