# Embedding Adaptation Lane

This lane is for replacing or improving the current `nomic-embed-text:latest` baseline used by mem0.

The current baseline is intentionally kept because it works. New embedding models should be tested in parallel collections or indexes, then promoted only after benchmark evidence.

## Work Items

1. Add candidate to `mem0/MODEL_CANDIDATES.yaml`.
2. Identify runtime path: Ollama, llama.cpp, LM Studio, MLX, Transformers, sentence-transformers, or custom service.
3. Record vector dimension and metric.
4. Create a new collection or index name.
5. Run `scripts/run_mem0_memory_benchmark.py`.
6. Run retrieval-specific benchmarks when feasible.
7. Compare latency and memory footprint against `nomic-embed-text:latest`.
8. Document rollback to `mem0_nomic_768`.

## Collection Naming

Use names that include model family and dimension:

| Model | Collection / index name |
|---|---|
| `nomic-embed-text:latest` | `mem0_nomic_768` |
| `BAAI/bge-m3` | `mem0_bge_m3_1024` |
| `Qwen/Qwen3-Embedding-4B` | `mem0_qwen3_embedding_4b_<dims>` |
| `jinaai/jina-embeddings-v4` | `mem0_jina_v4_<dims>` |
| `jinaai/jina-embeddings-v5-omni-small-mlx` | `mem0_jina_v5_omni_small_1024` |
| `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | `mem0_jina_v5_omni_small_1024` |
| `LiquidAI/LFM2-ColBERT-350M` | `mem0_lfm2_colbert_350m` |

Late-interaction models such as ColBERT do not use the same collection shape as dense embeddings.

## First Local Benchmark

For Ollama-served embedding models:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_suite.json
```

For OpenAI-compatible embedding servers such as Ollama `/v1`, LM Studio, or
`llama-server` where embeddings are enabled:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_embedding_benchmark.py \
  --base-url http://127.0.0.1:11434/v1 \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_suite.json
```

For Hugging Face embedding models that need `sentence-transformers`, install the
optional dependency set first:

```bash
source scripts/env.sh
python -m pip install -r requirements-mem0-embeddings.txt
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model BAAI/bge-m3 \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json
```

BGE-M3, Jina embeddings, and Qwen embedding candidates should start on this
path unless they are first exposed through a local OpenAI-compatible embedding
server.

The Jina v5 omni MLX variants are Apple Silicon-first candidates and should be
kept in a dedicated collection until local load/add/search behavior is proven.
Do not replace `mem0_nomic_768` with them by default.

For the Jina retrieval variant, prefix query text with `Query: ` and document
text with `Document: ` to match the model card's reference behavior. Keep the
text-matching variant unprefixed unless the model card says otherwise.

This benchmark is intentionally small. It is useful for quick regression checks and candidate triage; it is not a publication-quality retrieval score.

## Current Expanded Comparison

The 2026-05-26 expanded suite keeps `nomic-embed-text:latest` as the default
rollback embedder:

| Model | Dims | Top-1 | Recall@3 | p50 latency | Decision |
|---|---:|---:|---:|---:|---|
| `nomic-embed-text:latest` | 768 | 0.833 | 1.000 | 0.021s | keep default |
| `BAAI/bge-m3` | 1024 | 0.917 | 1.000 | 0.097s | side-by-side only |
| `jinaai/jina-embeddings-v5-omni-small-mlx` | 1024 | 0.833 | 1.000 | 0.020s | side-by-side only |
| `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | 1024 | 1.000 | 1.000 | 0.019s | side-by-side only |

Do not switch the live mem0 collection from `mem0_nomic_768` until a candidate
beats the expanded suite and has a larger live-read gate. BGE-M3 and Jina v5
remain useful for comparison, but their 1024-dimensional vectors require
dedicated collections such as `mem0_bge_m3_1024` or
`mem0_jina_v5_omni_small_1024`.

The 2026-06-13 isolated live fixture proved that the Jina text-matching MLX
model can be served locally through `scripts/jina_mlx_embedding_server.py` and
used by mem0's OpenAI embedder provider with an output-local 1024-dim Qdrant
collection. It still reached only 0.800 top-1 after close-margin reranking on
the live add/search fixture, so it remains side-by-side evidence rather than a
default replacement.

## Differentiation Gate

The 2026-06-13 differentiation suite adds harder near-duplicate operational
memory cases because the expanded suite was no longer separating candidates.

| Model | Dims | Top-1 | Recall@3 | p50 latency | Decision |
|---|---:|---:|---:|---:|---|
| `lmstudio-community/embeddinggemma-300m-qat-GGUF` | 768 | 1.000 | 1.000 | 1.154s | best isolated quality; needs batching/server and live mem0 proof |
| `BAAI/bge-m3` | 1024 | 0.929 | 1.000 | 0.115s | strongest current differentiator; still side-by-side only |
| `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | 1024 | 0.786 | 0.929 | 0.026s | fast but missed role/path/runtime boundary cases |
| `nomic-embed-text:latest` | 768 | 0.714 | 0.857 | 0.020s | keep default rollback, but not the quality leader on this suite |

Use `benchmarks/embeddings/memory_retrieval_differentiation_suite.json` for
future promotion claims. It now contains 14 near-duplicate operational memory
cases; the older expanded suite remains a regression gate, not the final
differentiator.
The EmbeddingGemma GGUF result proves a high-quality 768-dim candidate, but the
current runner shells out to `llama-embedding` per text. Promote only after a
batched or server-backed path passes live mem0 add/search and rollback checks.
