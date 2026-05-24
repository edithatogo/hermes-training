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
| 2 | `sam860/LFM2:2.6b` | extractor | working-default | ollama | extraction-smoke | baseline; keep as rollback and compare only |
| 3 | `hermes3:8b` | extractor | installed-baseline | ollama | extraction-smoke | baseline; keep as rollback and compare only |
| 4 | `Qwen/Qwen3-Reranker-4B` | reranker | candidate | transformers | rerank-smoke | requires model acquisition/load proof; fixed-candidate harness is ready |
| 5 | `mem0-created-at-rank-reranker` | reranker | candidate | local-python | rerank-smoke | none recorded |
| 6 | `BAAI/bge-m3` | embedder | candidate | sentence-transformers | mteb-retrieval-smoke | requires model acquisition/load proof and memory-footprint check |
| 7 | `Qwen/Qwen3-Embedding-4B` | embedder | candidate | transformers | local-embedding-smoke | requires model acquisition/load proof and memory-footprint check |
| 8 | `jinaai/jina-embeddings-v4` | embedder | candidate | sentence-transformers | mteb-retrieval-smoke | requires model acquisition/load proof and memory-footprint check |
| 9 | `LiquidAI/LFM2-ColBERT-350M` | retriever | candidate | transformers | colbert-index-smoke | needs separate index/service shape |
| 10 | `NousResearch/Hermes-4-14B` | extractor | runtime-proof-needed | ollama-gguf | endpoint-smoke | needs local artifact or endpoint proof |

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
- Status: `working-default`
- Blocker: baseline; keep as rollback and compare only

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model sam860/LFM2:2.6b \
  --base-url http://127.0.0.1:11434/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-sam860-lfm2-2-6b-$(date +%Y%m%d-%H%M%S)
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
# First install optional reranker deps if needed.
python -m pip install -r requirements-mem0-rerankers.txt
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy cross_encoder \
  --model Qwen/Qwen3-Reranker-4B \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id rerank-qwen-qwen3-reranker-4b-$(date +%Y%m%d-%H%M%S)
```

### mem0-created-at-rank-reranker

- Role: `reranker`
- Status: `candidate`
- Blocker: none recorded

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool cmd \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --rerank-strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id mem0-mem0-created-at-rank-reranker-$(date +%Y%m%d-%H%M%S)
```

### BAAI/bge-m3

- Role: `embedder`
- Status: `candidate`
- Blocker: requires model acquisition/load proof and memory-footprint check

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

### LiquidAI/LFM2-ColBERT-350M

- Role: `retriever`
- Status: `candidate`
- Blocker: needs separate index/service shape

```bash
source scripts/env.sh
# Build a separate retriever service/index before benchmarking.
# Do not reuse the dense Qdrant collection for late-interaction vectors.
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
