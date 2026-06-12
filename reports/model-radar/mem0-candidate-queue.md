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
| 5 | `onnx-community/Qwen3-Reranker-0.6B-ONNX` | reranker | source-model-benchmarked | onnxruntime | expanded-derived-rerank | source Qwen/Qwen3-Reranker-0.6B fixed LFM2-ColBERT expanded retrieval to top-1 1.000; ONNX package remains blocked pending bounded CPU/CoreML proof |
| 6 | `BAAI/bge-m3` | embedder | benchmarked-cpu-mps-not-promoted | sentence-transformers | mteb-retrieval-smoke | benchmarked but not promoted; keep separate collection or artifact |
| 7 | `NousResearch/Hermes-4-14B` | extractor | runtime-proven-extraction-needed | llama.cpp-gguf | extraction-smoke | local GGUF runtime proof exists; needs mem0 extraction benchmark before extractor promotion |
| 8 | `hermes3:8b` | extractor | installed-baseline | ollama | extraction-smoke | baseline; keep as rollback and compare only |
| 9 | `Qwen/Qwen3-Reranker-4B` | reranker | source-model-benchmarked | transformers | expanded-derived-rerank | 2026-06-12 CPU expanded-derived rerank passed at top-1 1.000 / recall@3 1.000; p50 4.943s, so keep as quality ceiling until accelerated/live replay proof |
| 10 | `flaglow/BAAI-bge-reranker-v2-m3-mlx-fp16` | reranker | candidate-runtime-id-verified | mlx | mlx-load-smoke | model repo verified; MLX load/scoring proof is ready before live mem0 integration |
| 11 | `Qwen/Qwen3-Embedding-4B` | embedder | source-model-benchmarked | transformers | expanded-embedding-suite | 2026-06-12 CPU expanded suite reached top-1 0.917 / recall@3 1.000 with 2560-dim embeddings; p50 1.534s |
| 12 | `google/embeddinggemma-300m` | embedder | access-gated | sentence-transformers | mteb-retrieval-smoke | 2026-06-12 direct smoke returned Hugging Face gated repo 403; requires account access before benchmark |
| 13 | `jinaai/jina-embeddings-v4` | embedder | runtime-blocked | sentence-transformers | mteb-retrieval-smoke | trust-remote-code path needs pillow/peft and still fails on SlidingWindowCache import in current Transformers stack |
| 14 | `jinaai/jina-embeddings-v5-omni-small-mlx` | embedder | candidate | mlx | local-embedding-smoke | 2026-06-11 retrieval smoke passed at top-1 1.000 / recall@3 1.000 / MRR 1.000 on the 1-case metadata-database query with 1024-dim embeddings; verify collection shape before any default switch |
| 15 | `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | embedder | source-model-benchmarked | mlx | expanded-embedding-suite | 2026-06-12 expanded suite reached top-1 1.000 / recall@3 1.000 with 1024-dim embeddings and p50 0.019s; not promoted until 1024-dim collection migration plus live add/search rollback proof |
| 16 | `LiquidAI/LFM2-ColBERT-350M` | retriever | source-model-benchmarked | transformers | expanded-retriever-suite | 2026-06-12 expanded retriever suite reached top-1 0.917 / recall@3 1.000; isolated mem0 fixture reached top-1 0.833 on 3-5 candidate sets, trailing close-margin 1.000; keep opt-in |

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

### onnx-community/Qwen3-Reranker-0.6B-ONNX

- Role: `reranker`
- Status: `source-model-benchmarked`
- Evidence: `reports/benchmark/mem0/lfm2-colbert-qwen3-06b-rerank-20260612.md`
- Blocker: source Qwen/Qwen3-Reranker-0.6B passed suites, including LFM2-ColBERT expanded-derived reranking; ONNX package remains blocked pending bounded CPU/CoreML proof

```bash
source scripts/env.sh
HF_HOME=/Volumes/PortableSSD/huggingface HF_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub \
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device cpu \
  --qwen3-max-length 1024 \
  --suite /Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/lfm2-colbert-expanded-derived-reranking-20260612/candidate-suite.json \
  --run-id lfm2-colbert-qwen3-06b-rerank-$(date +%Y%m%d)
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
- Status: `runtime-proven-extraction-needed`
- Runtime evidence: `reports/runtime/hermes4-14b-q4-llamacpp-smoke-20260524.md`
- Benchmark evidence: `reports/benchmark/endpoint-pilots/hermes4-14b-q4-llamacpp-pilots-20260524.md`
- Blocker: local Hermes 4 GGUF runtime exists, but mem0 extraction quality has not been benchmarked against the LFM2 rollback extractor

```bash
source scripts/env.sh
# First expose the local Hermes 4 GGUF through an OpenAI-compatible
# /v1/chat/completions endpoint, then run:
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model hermes-4-14b-q4 \
  --base-url http://127.0.0.1:8092/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-hermes4-14b-q4-smoke-$(date +%Y%m%d-%H%M%S)
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
- Status: `source-model-benchmarked`
- Evidence: `reports/benchmark/mem0/qwen3-4b-expanded-rerank-20260612.md`
- Blocker: quality proof passed, but CPU p50 4.943s / p95 10.564s on the expanded-derived suite is too heavy for default promotion without live replay or acceleration

```bash
source scripts/env.sh
HF_HOME=/Volumes/PortableSSD/huggingface HF_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub \
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-4B \
  --qwen3-device cpu \
  --qwen3-max-length 1024 \
  --suite /Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/qwen3-4b-expanded-derived-reranking-20260612/candidate-suite.json \
  --run-id qwen3-4b-expanded-rerank-$(date +%Y%m%d)
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
- Status: `source-model-benchmarked`
- Evidence: `reports/benchmark/mem0/embedding-qwen3-4b-expanded-20260612.md`
- Blocker: expanded suite reached top-1 0.917 and missed one recency case, so it requires reranking plus a separate 2560-dim collection before any default switch

```bash
source scripts/env.sh
HF_HOME=/Volumes/PortableSSD/huggingface HF_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub \
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model Qwen/Qwen3-Embedding-4B \
  --device cpu \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --run-id embedding-qwen3-4b-expanded-$(date +%Y%m%d)
```

### google/embeddinggemma-300m

- Role: `embedder`
- Status: `access-gated`
- Evidence: `reports/benchmark/mem0/embedding-google-embeddinggemma-300m-blocked-20260612.md`
- Blocker: Hugging Face returned a gated repo 403 on 2026-06-12; benchmark cannot run until the account has access

```bash
source scripts/env.sh
HF_HOME=/Volumes/PortableSSD/huggingface HF_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub \
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model google/embeddinggemma-300m \
  --device cpu \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-google-embeddinggemma-300m-$(date +%Y%m%d-%H%M%S)
```

### jinaai/jina-embeddings-v4

- Role: `embedder`
- Status: `runtime-blocked`
- Evidence: `reports/benchmark/mem0/embedding-jina-v4-runtime-blocked-20260612.md`
- Blocker: trust-remote-code load gets past custom modules after pillow/peft are installed, then fails on `SlidingWindowCache` import in the current Transformers stack

```bash
source scripts/env.sh
HF_HOME=/Volumes/PortableSSD/huggingface HF_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub \
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v4 \
  --device cpu \
  --trust-remote-code \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-jinaai-jina-embeddings-v4-$(date +%Y%m%d-%H%M%S)
```

### jinaai/jina-embeddings-v5-omni-small-mlx

- Role: `embedder`
- Status: `candidate`
- Blocker: 2026-06-11 retrieval smoke passed at top-1 1.000 / recall@3 1.000 / MRR 1.000 on the 1-case metadata-database query with 1024-dim embeddings; verify collection shape before any default switch

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
- Blocker: expanded suite passed at top-1 1.000 / recall@3 1.000 with p50 0.019s, but default promotion requires a 1024-dim collection migration plan plus live add/search rollback proof

```bash
source scripts/env.sh
# Jina MLX embeddings are custom-code repos; load them through the dedicated MLX benchmark runner.
./.venv/bin/python scripts/run_jina_mlx_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v5-omni-small-text-matching-mlx \
  --task-type text-matching \
  --repo-dir /Volumes/PortableSSD/huggingface/hub/jina-mlx/jina-mlx-text-matching-smoke-20260612b \
  --local-files-only \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --run-id jina-mlx-text-matching-expanded-$(date +%Y%m%d-%H%M%S)
```

### LiquidAI/LFM2-ColBERT-350M

- Role: `retriever`
- Status: `source-model-benchmarked`
- Blocker: opt-in read-wrapper mode and service-down fallback exist; multi-result fixture is now proven but trails the close-margin default on recency-sensitive memory
- Evidence: `reports/benchmark/mem0/retriever-lfm2-colbert-expanded-20260612.md`
- Wrapper smoke: `reports/benchmark/mem0/colbert-read-wrapper-smoke-20260612.md`
- Fallback smoke: `reports/benchmark/mem0/colbert-service-down-fallback-20260612.md`
- Lifecycle smoke: `reports/benchmark/mem0/mem0-colbert-stack-20260612-read-stack-smoke.md`
- Multi-result fixture: `reports/benchmark/mem0/mem0-live-fixture-colbert-rerank-20260612.md`

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_retriever_service_benchmark.py \
  --base-url http://127.0.0.1:8765 \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --run-id retriever-lfm2-colbert-expanded-$(date +%Y%m%d)

./.venv/bin/python scripts/run_colbert_read_stack_smoke.py \
  --local-files-only \
  --run-id-prefix mem0-colbert-stack-$(date +%Y%m%d-%H%M%S)
```
