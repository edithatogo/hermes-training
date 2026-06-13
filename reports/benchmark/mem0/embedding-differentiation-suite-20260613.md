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
| `benchmarks/embeddings/memory_retrieval_differentiation_suite.json` | 14 | Isolated embedding retrieval with six close documents per query |
| `benchmarks/mem0_memory/live_fixture_differentiation_suite.json` | 11 | Real mem0 add/search fixture with four setup memories per query |

## Embedding Results

| Model | Runtime | Dims | Top-1 | Recall@3 | MRR | nDCG@3 | p50 embed |
|---|---|---:|---:|---:|---:|---:|---:|
| `lmstudio-community/embeddinggemma-300m-qat-GGUF` | llama.cpp `llama-server` OpenAI embeddings | 768 | 1.000 | 1.000 | 1.000 | 1.000 | 0.012s |
| `lmstudio-community/embeddinggemma-300m-qat-GGUF` | llama.cpp `llama-embedding` GGUF | 768 | 1.000 | 1.000 | 1.000 | 1.000 | 1.154s |
| `BAAI/bge-m3` | sentence-transformers CPU | 1024 | 0.929 | 1.000 | 0.952 | 0.964 | 0.115s |
| `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | MLX cached local files | 1024 | 0.786 | 0.929 | 0.875 | 0.876 | 0.026s |
| `nomic-embed-text:latest` | Ollama | 768 | 0.714 | 0.857 | 0.821 | 0.804 | 0.020s |

## Miss Patterns

| Model | Missed top-1 cases |
|---|---|
| `lmstudio-community/embeddinggemma-300m-qat-GGUF` | none |
| `BAAI/bge-m3` | `runtime-validation-boundary` |
| `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | `embedder-default-vs-best-score`, `storage-artifact-boundary`, `runtime-validation-boundary` |
| `nomic-embed-text:latest` | `dataset-publish-scope`, `storage-artifact-boundary`, `runtime-validation-boundary`, `azure-quota-no-compute` |

## Live mem0 Fixture Result

| Strategy | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | Distractor resistance |
|---|---:|---:|---:|---:|---:|---:|
| `EmbeddingGemma GGUF via llama.cpp server wrapper` | 0.909 | 1.000 | 0.955 | 0.966 | 1.000 | 0.750 |
| `EmbeddingGemma GGUF via resilient llama.cpp proxy` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `vector` | 0.818 | 0.909 | 0.848 | 0.864 | 0.500 | 0.750 |
| `score_plus_created_at_rank_close_margin` | 0.636 | 0.909 | 0.742 | 0.785 | 0.500 | 0.500 |

The live fixture used an output-local `MEM0_CONFIG_PATH`, isolated Qdrant path,
and no default collection mutation. The expanded fixture shows that the
close-margin wrapper is not always safer than raw vector ordering. The first
direct EmbeddingGemma server wrapper used the same output-local fixture pattern
and reached 0.909 top-1 with 4-5 candidates per query, but it still missed the
GGUF runtime-boundary distractor case. The later resilient-proxy path fixed the
server lifetime and local HOME isolation issues and reached 1.000 top-1.

## EmbeddingGemma Replay Rerank Gate

| Replay strategy | Source candidates | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | Distractor resistance |
|---|---|---:|---:|---:|---:|---:|---:|
| `vector` | captured live fixture vector candidates | 0.909 | 1.000 | 0.955 | 0.966 | 1.000 | 0.750 |
| `query_terms_guarded` | captured live fixture vector candidates | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

The replay gate rebuilds fixed candidates from
`mem0-live-fixture-embeddinggemma-llamacpp-server-wrapper-20260613/results.jsonl`
and does not re-add memories or mutate a collection. It proves that the
remaining EmbeddingGemma miss is a reranking policy issue rather than an
embedding recall issue: the target answer was already within the top 3, while
the raw vector top result was a negated "not the GGUF runtime path" distractor.
The replay result was used as the diagnostic gate before the fresh live proxy
fixture below.

## EmbeddingGemma Live Proxy Gate

The fresh live fixture
`mem0-live-fixture-embeddinggemma-query-guard-pathfix-20260613` used
`scripts/run_resilient_llama_cpp_embedding_proxy.py` in front of `llama-server`
because the direct server wrapper exited cleanly after repeated embedding
requests. The proxy-backed run kept the fixture output-local and did not mutate
the default `mem0_nomic_768` collection.

It also used a patched isolated fixture harness that runs mem0 subprocesses
through a fixture-local `$HOME/.mem0` copy and direct `mem0_wrapper.py` calls.
This avoids global Qdrant migration-lock collisions while preserving the
installed mem0 package through `PYTHONPATH`.

| Strategy | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | Distractor resistance |
|---|---:|---:|---:|---:|---:|---:|
| `vector` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `score_plus_created_at_rank_close_margin` | 0.909 | 1.000 | 0.939 | 0.955 | 1.000 | 0.750 |
| `query_terms_guarded` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

This closes the immediate live fixture blocker for the EmbeddingGemma GGUF
candidate. It is still not a default replacement until the resilient proxy path
is integrated deliberately, rollback behavior is documented, and the default
collection migration decision is made.

## Raw Evidence

| Run | Output |
|---|---|
| `embedding-bge-m3-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-differentiation-20260613` |
| `embedding-bge-m3-differentiation-expanded-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-differentiation-expanded-20260613` |
| `jina-mlx-text-matching-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-differentiation-20260613` |
| `jina-mlx-text-matching-differentiation-expanded-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/jina-mlx-text-matching-differentiation-expanded-20260613` |
| `embedding-nomic-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-differentiation-20260613` |
| `embedding-nomic-differentiation-expanded-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-differentiation-expanded-20260613` |
| `embeddinggemma-300m-qat-gguf-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embeddinggemma-300m-qat-gguf-differentiation-20260613` |
| `embeddinggemma-300m-qat-llamacpp-wrapper-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embeddinggemma-300m-qat-llamacpp-wrapper-differentiation-20260613` |
| `mem0-live-fixture-differentiation-20260613` | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-differentiation-20260613` |
| `mem0-live-fixture-differentiation-expanded-20260613` | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-differentiation-expanded-20260613` |
| `mem0-live-fixture-embeddinggemma-llamacpp-server-wrapper-20260613` | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-embeddinggemma-llamacpp-server-wrapper-20260613` |
| `embeddinggemma-fixture-replay-vector-20260613` | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/embeddinggemma-fixture-replay-vector-20260613` |
| `embeddinggemma-fixture-replay-query-guard-20260613` | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/embeddinggemma-fixture-replay-query-guard-20260613` |
| `mem0-live-fixture-embeddinggemma-query-guard-pathfix-20260613` | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-embeddinggemma-query-guard-pathfix-20260613` |

## Decision

Use the differentiation suite for future mem0 embedder and reranker promotion
claims. The older expanded suite remains a regression gate, but it is no
longer sufficient on its own because it lets too many candidates converge on
similar scores.
