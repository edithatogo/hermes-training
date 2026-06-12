# mem0 Candidate Execution Queue

Target: Local mem0 memory for Codex, Cline, Hermes, and other CLI agents

## Current Default

| Component | Value |
|---|---|
| vector_store | `qdrant` |
| collection | `mem0_nomic_768` |
| embedder | `nomic-embed-text:latest` |
| embedder_runtime | `ollama` |
| embedding_dims | `768` |
| extractor | `sam860/LFM2:2.6b` |
| extractor_runtime | `ollama` |
| status | `working-default` |

## Queue

| Priority | Candidate | Role | Status | First runtime | First gate | Blocker / note |
|---:|---|---|---|---|---|---|
| 1 | `nomic-embed-text:latest` | embedder | working-default | ollama | add-search-smoke | baseline; keep as rollback and compare only |
| 2 | `sam860/LFM2:2.6b` | extractor | working-default-clean-root-smoked | ollama | extraction-smoke | baseline recovered in clean SSD Ollama root; keep as rollback and compare only |
| 3 | `flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` | reranker | isolated-fixture-proven | mlx | multi-query-cold-warm-latency-probe | first bounded cache-hit daily-use probe passed; keep opt-in read mode until broader cold/warm latency proof |
| 4 | `mem0-created-at-rank-reranker` | reranker | live-read-wrapper-smoked | local-python | rerank-smoke | live read-only wrapper smoke passed; keep read-only until broader coverage |
| 5 | `Qwen/Qwen3-Reranker-4B` | reranker | source-model-benchmarked | transformers | rerank-smoke | quality proof passed, but CPU latency is too high for default promotion without acceleration or live replay proof |
| 6 | `onnx-community/Qwen3-Reranker-0.6B-ONNX` | reranker | source-model-benchmarked | onnxruntime | rerank-smoke | source Qwen/Qwen3-Reranker-0.6B passed suites; ONNX package remains blocked pending bounded CPU/CoreML proof |
| 7 | `BAAI/bge-m3` | embedder | benchmarked-cpu-mps-not-promoted | sentence-transformers | differentiation-suite | expanded 2026-06-13 differentiation suite reached top-1 0.929 / recall@3 1.000, strongest current embedder signal; keep separate 1024-dim collection |
| 8 | `Qwen/Qwen3-Embedding-4B` | embedder | source-model-benchmarked | transformers | local-embedding-smoke | expanded suite passed recall but missed one top-1 recency case; keep behind separate 2560-dim collection and reranking |
| 9 | `jinaai/jina-embeddings-v5-omni-small-mlx` | embedder | source-model-benchmarked | mlx | local-embedding-smoke | expanded retrieval suite reached recall 1.000 but top-1 0.833 with two close recency/update misses; prefer text-matching variant for now |
| 10 | `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | embedder | source-model-benchmarked | mlx | differentiation-suite | expanded suite passed at 1.000, but expanded 2026-06-13 differentiation suite reached top-1 0.786 / recall@3 0.929; keep as fast candidate, not default |
| 11 | `NousResearch/Hermes-4-14B` | extractor | extraction-benchmarked-not-promoted | ollama-gguf | extraction-smoke | extraction benchmark completed but failed promotion gate; keep LFM2 as the default extractor |
| 12 | `LiquidAI/LFM2-ColBERT-350M` | retriever | source-model-benchmarked | transformers | colbert-index-smoke | expanded retriever benchmark completed; keep opt-in because isolated mem0 fixture trailed close-margin guarded read |
| 13 | `hermes3:8b` | extractor | installed-baseline | ollama | extraction-smoke | baseline; keep as rollback and compare only |
| 14 | `flaglow/BAAI-bge-reranker-v2-m3-mlx-fp16` | reranker | candidate-runtime-id-verified | mlx | mlx-load-smoke | model repo verified; MLX load/scoring proof is ready before live mem0 integration |
| 15 | `google/embeddinggemma-300m` | embedder | access-gated | sentence-transformers | mteb-retrieval-smoke | Official Google retrieval baseline for mem0 comparison. Gated model with 2048-token context and configurable 128-768 embedding dimensions; the first direct smoke returned a Hugging Face 403, so keep it behind a separate collection until access is granted and a challenger wins on quality, latency, and migration cost |
| 16 | `jinaai/jina-embeddings-v4` | embedder | runtime-blocked | sentence-transformers | mteb-retrieval-smoke | requires model acquisition/load proof and memory-footprint check |

## Candidate Commands

### nomic-embed-text:latest

- Role: `embedder`
- Status: `working-default`
- Blocker: baseline; keep as rollback and compare only

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-nomic-embed-text-latest-$(date +%Y%m%d-%H%M%S)
```

### sam860/LFM2:2.6b

- Role: `extractor`
- Status: `working-default-clean-root-smoked`
- Blocker: baseline recovered in clean SSD Ollama root; keep as rollback and compare only

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model sam860/LFM2:2.6b \
  --base-url http://127.0.0.1:11434/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-sam860-lfm2-2-6b-$(date +%Y%m%d-%H%M%S)
```

### flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit

- Role: `reranker`
- Status: `isolated-fixture-proven`
- Blocker: first bounded cache-hit daily-use probe passed; keep opt-in read mode until broader cold/warm latency proof

```bash
source scripts/env.sh
# Opt-in guarded read mode is available; run bounded cold/warm latency probes before any default integration.
HF_HUB_DISABLE_XET=1 ./.venv/bin/python scripts/run_mem0_read_latency_probe.py \
  --mode mlx-bge \
  --query "What is the active mem0 Qdrant collection?" \
  --iterations 1 \
  --read-wall-timeout-s 60 \
  --subprocess-read \
  --fallback-to-vector \
  --cache-ttl-s 300
```

### mem0-created-at-rank-reranker

- Role: `reranker`
- Status: `live-read-wrapper-smoked`
- Blocker: live read-only wrapper smoke passed; keep read-only until broader coverage

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy score_plus_created_at_rank_close_margin \
  --recency-weight 0.20 \
  --timeout-s 60
```

### Qwen/Qwen3-Reranker-4B

- Role: `reranker`
- Status: `source-model-benchmarked`
- Blocker: quality proof passed, but CPU latency is too high for default promotion without acceleration or live replay proof

```bash
source scripts/env.sh
# First ensure the model is available in the SSD Hugging Face cache.
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-4B \
  --qwen3-device auto \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id rerank-qwen-qwen3-reranker-4b-$(date +%Y%m%d-%H%M%S)
```

### onnx-community/Qwen3-Reranker-0.6B-ONNX

- Role: `reranker`
- Status: `source-model-benchmarked`
- Blocker: source Qwen/Qwen3-Reranker-0.6B passed suites; ONNX package remains blocked pending bounded CPU/CoreML proof

```bash
source scripts/env.sh
# ONNX candidate is Transformers.js-oriented; this fail-closed bridge proof keeps Node tooling on the SSD.
./.venv/bin/python scripts/run_qwen3_onnx_transformersjs_smoke.py \
  --run-id qwen3-0-6b-onnx-transformersjs-$(date +%Y%m%d-%H%M%S) \
  --limit-cases 1 \
  --max-length 512 \
  --timeout-s 180
```

### BAAI/bge-m3

- Role: `embedder`
- Status: `benchmarked-cpu-mps-not-promoted`
- Blocker: benchmarked but not promoted; keep separate collection or artifact

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model BAAI/bge-m3 \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-baai-bge-m3-$(date +%Y%m%d-%H%M%S)
```

### Qwen/Qwen3-Embedding-4B

- Role: `embedder`
- Status: `source-model-benchmarked`
- Blocker: expanded suite passed recall but missed one top-1 recency case; keep behind separate 2560-dim collection and reranking

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model Qwen/Qwen3-Embedding-4B \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-qwen-qwen3-embedding-4b-$(date +%Y%m%d-%H%M%S)
```

### jinaai/jina-embeddings-v5-omni-small-mlx

- Role: `embedder`
- Status: `source-model-benchmarked`
- Blocker: expanded retrieval suite reached recall 1.000 but top-1 0.833 with two close recency/update misses; prefer text-matching variant for now

```bash
source scripts/env.sh
# Jina MLX embeddings are custom-code repos; clone and load them through the dedicated MLX benchmark runner.
./.venv/bin/python scripts/run_jina_mlx_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v5-omni-small-mlx \
  --task-type retrieval \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-jinaai-jina-embeddings-v5-omni-small-mlx-$(date +%Y%m%d-%H%M%S)
```

### jinaai/jina-embeddings-v5-omni-small-text-matching-mlx

- Role: `embedder`
- Status: `source-model-benchmarked`
- Blocker: expanded suite passed at 1.000 with fast 1024-dim MLX embeddings; requires collection migration plus live add/search rollback proof before default switch

```bash
source scripts/env.sh
# Jina MLX embeddings are custom-code repos; clone and load them through the dedicated MLX benchmark runner.
./.venv/bin/python scripts/run_jina_mlx_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v5-omni-small-text-matching-mlx \
  --task-type text-matching \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-jinaai-jina-embeddings-v5-omni-small-text-matching-mlx-$(date +%Y%m%d-%H%M%S)
```

### NousResearch/Hermes-4-14B

- Role: `extractor`
- Status: `extraction-benchmarked-not-promoted`
- Blocker: extraction benchmark completed but failed promotion gate; keep LFM2 as the default extractor

```bash
source scripts/env.sh
# Hermes 4 Q4 has already failed this gate at 2/7; rerun only after a prompt/template change.
# First expose the local Hermes 4 GGUF through llama.cpp on http://127.0.0.1:8092/v1.
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model hermes-4-14b-q4 \
  --base-url http://127.0.0.1:8092/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-hermes4-14b-q4-smoke-$(date +%Y%m%d-%H%M%S)
```

### LiquidAI/LFM2-ColBERT-350M

- Role: `retriever`
- Status: `source-model-benchmarked`
- Blocker: expanded retriever benchmark completed; keep opt-in because isolated mem0 fixture trailed close-margin guarded read

```bash
source scripts/env.sh
# Build a separate retriever service/index before benchmarking.
# Do not reuse the dense Qdrant collection for late-interaction vectors.
```

### hermes3:8b

- Role: `extractor`
- Status: `installed-baseline`
- Blocker: baseline; keep as rollback and compare only

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model hermes3:8b \
  --base-url http://127.0.0.1:11434/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-hermes3-8b-$(date +%Y%m%d-%H%M%S)
```

### flaglow/BAAI-bge-reranker-v2-m3-mlx-fp16

- Role: `reranker`
- Status: `candidate-runtime-id-verified`
- Blocker: model repo verified; MLX load/scoring proof is ready before live mem0 integration

```bash
source scripts/env.sh
# MLX BGE reranker repo ID is verified. Run a bounded Apple Silicon load/scoring proof first.
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy mlx_cross_encoder \
  --model flaglow/BAAI-bge-reranker-v2-m3-mlx-fp16 \
  --mlx-max-length 1024 \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id rerank-flaglow-baai-bge-reranker-v2-m3-mlx-fp16-$(date +%Y%m%d-%H%M%S)
```

### google/embeddinggemma-300m

- Role: `embedder`
- Status: `access-gated`
- Blocker: Official Google retrieval baseline for mem0 comparison. Gated model with 2048-token context and configurable 128-768 embedding dimensions; the first direct smoke returned a Hugging Face 403, so keep it behind a separate collection until access is granted and a challenger wins on quality, latency, and migration cost

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model google/embeddinggemma-300m \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-google-embeddinggemma-300m-$(date +%Y%m%d-%H%M%S)
```

### jinaai/jina-embeddings-v4

- Role: `embedder`
- Status: `runtime-blocked`
- Blocker: requires model acquisition/load proof and memory-footprint check

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v4 \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-jinaai-jina-embeddings-v4-$(date +%Y%m%d-%H%M%S)
```
