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

This benchmark is intentionally small. It is useful for quick regression checks and candidate triage; it is not a publication-quality retrieval score.

## Current Expanded Comparison

The 2026-05-26 expanded suite keeps `nomic-embed-text:latest` as the default
rollback embedder:

| Model | Dims | Top-1 | Recall@3 | p50 latency | Decision |
|---|---:|---:|---:|---:|---|
| `nomic-embed-text:latest` | 768 | 0.833 | 1.000 | 0.021s | keep default |
| `BAAI/bge-m3` | 1024 | 0.917 | 1.000 | 0.097s | side-by-side only |

Do not switch the live mem0 collection from `mem0_nomic_768` until a candidate
beats the expanded suite and has a larger live-read gate. BGE-M3 remains useful
for comparison, but its 1024-dimensional vectors require `mem0_bge_m3_1024`.
