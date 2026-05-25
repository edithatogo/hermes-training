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
| 3 | `flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` | reranker | isolated-fixture-proven | mlx | daily-use-latency-probe | isolated fixture passed; keep opt-in read mode until broader daily-use latency proof |
| 4 | `mem0-created-at-rank-reranker` | reranker | live-read-wrapper-smoked | local-python | rerank-smoke | live read-only wrapper smoke passed; keep read-only until broader coverage |
| 5 | `onnx-community/Qwen3-Reranker-0.6B-ONNX` | reranker | source-model-benchmarked | onnxruntime | rerank-smoke | source Qwen/Qwen3-Reranker-0.6B passed suites; ONNX package remains blocked pending bounded CPU/CoreML proof |
| 6 | `BAAI/bge-m3` | embedder | benchmarked-cpu-mps-not-promoted | sentence-transformers | mteb-retrieval-smoke | benchmarked but not promoted; keep separate collection or artifact |
| 7 | `NousResearch/Hermes-4-14B` | extractor | runtime-proof-needed | ollama-gguf | endpoint-smoke | needs local artifact or endpoint proof |
| 8 | `hermes3:8b` | extractor | installed-baseline | ollama | extraction-smoke | baseline; keep as rollback and compare only |
| 9 | `Qwen/Qwen3-Reranker-4B` | reranker | candidate | transformers | rerank-smoke | requires model acquisition/load proof; fixed-candidate harness is ready |
| 10 | `flaglow/BAAI-bge-reranker-v2-m3-mlx-fp16` | reranker | candidate-runtime-id-verified | mlx | mlx-load-smoke | model repo verified; MLX load/scoring proof is ready before live mem0 integration |
| 11 | `Qwen/Qwen3-Embedding-4B` | embedder | candidate | transformers | local-embedding-smoke | requires model acquisition/load proof and memory-footprint check |
| 12 | `jinaai/jina-embeddings-v4` | embedder | candidate | sentence-transformers | mteb-retrieval-smoke | requires model acquisition/load proof and memory-footprint check |
| 13 | `jinaai/jina-embeddings-v5-omni-small-mlx` | embedder | candidate | mlx | local-embedding-smoke | verify embedding dimension before creating collection |
| 14 | `LiquidAI/LFM2-ColBERT-350M` | retriever | candidate | transformers | colbert-index-smoke | needs separate index/service shape |

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
- Blocker: isolated fixture passed; keep opt-in read mode until broader daily-use latency proof

```bash
source scripts/env.sh
# Opt-in guarded read mode is available; run daily-use latency probes before any default integration.
HF_HUB_DISABLE_XET=1 ./.venv/bin/python scripts/mem0_read.py \
  "What is the active mem0 Qdrant collection?" \
  --mode mlx-bge \
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

### NousResearch/Hermes-4-14B

- Role: `extractor`
- Status: `runtime-proof-needed`
- Blocker: needs local artifact or endpoint proof

```bash
source scripts/env.sh
# First create or load a local runtime artifact for this model.
# Then expose it through an OpenAI-compatible /v1/chat/completions endpoint.
# After endpoint proof, run:
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model <local-model-id> \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-nousresearch-hermes-4-14b-$(date +%Y%m%d-%H%M%S)
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

### Qwen/Qwen3-Reranker-4B

- Role: `reranker`
- Status: `candidate`
- Blocker: requires model acquisition/load proof; fixed-candidate harness is ready

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

### Qwen/Qwen3-Embedding-4B

- Role: `embedder`
- Status: `candidate`
- Blocker: requires model acquisition/load proof and memory-footprint check

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model Qwen/Qwen3-Embedding-4B \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-qwen-qwen3-embedding-4b-$(date +%Y%m%d-%H%M%S)
```

### jinaai/jina-embeddings-v4

- Role: `embedder`
- Status: `candidate`
- Blocker: requires model acquisition/load proof and memory-footprint check

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v4 \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-jinaai-jina-embeddings-v4-$(date +%Y%m%d-%H%M%S)
```

### jinaai/jina-embeddings-v5-omni-small-mlx

- Role: `embedder`
- Status: `candidate`
- Blocker: verify embedding dimension before creating collection

```bash
source scripts/env.sh
# No default command yet.
```

### LiquidAI/LFM2-ColBERT-350M

- Role: `retriever`
- Status: `candidate`
- Blocker: needs separate index/service shape

```bash
source scripts/env.sh
# Build a separate retriever service/index before benchmarking.
# Do not reuse the dense Qdrant collection for late-interaction vectors.
```
