# mem0 Benchmark Manifest

Date: 2026-05-24

## Purpose

Track memory, embedding, reranking, and extraction benchmarks for the local mem0 lane.

## Current Required Commands

### Candidate Queue

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_mem0_candidate_queue.py
```

### Memory Recency With Inline Reranking

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool cmd \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --rerank-strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id mem0-current-nomic-recency-reranked-$(date +%Y%m%d-%H%M%S)
```

### Fixed Candidate Reranking

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id fixed-rerank-created-at-rank-$(date +%Y%m%d-%H%M%S)
```

### Direct Ollama Embedding

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-nomic-smoke-$(date +%Y%m%d-%H%M%S)
```

### OpenAI-Compatible Embedding Endpoint

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_embedding_benchmark.py \
  --base-url http://127.0.0.1:11434/v1 \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-nomic-openai-$(date +%Y%m%d-%H%M%S)
```

### sentence-transformers Embedding Candidate

```bash
source scripts/env.sh
python -m pip install -r requirements-mem0-embeddings.txt
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model BAAI/bge-m3 \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-bge-m3-$(date +%Y%m%d-%H%M%S)
```

### Ollama Memory Extraction

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_memory_extraction_benchmark.py \
  --model 'sam860/LFM2:2.6b' \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-lfm2-2-6b-smoke-$(date +%Y%m%d-%H%M%S)
```

Use `scripts/run_openai_memory_extraction_benchmark.py` with the same arguments
for LM Studio, `llama-server`, or another OpenAI-compatible chat server.

### Benchmark Index

```bash
source scripts/env.sh
./.venv/bin/python scripts/summarize_mem0_benchmarks.py \
  /Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/*/summary.json \
  /Volumes/PortableSSD/hermes-evals/embedding-benchmark/*/summary.json \
  /Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/*/summary.json \
  /Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/*/summary.json \
  --output reports/benchmark/mem0/index.md
```

### Run Card

```bash
source scripts/env.sh
./.venv/bin/python scripts/create_mem0_run_card.py \
  /Volumes/PortableSSD/hermes-evals/<benchmark-kind>/<run-id>/summary.json \
  --output reports/benchmark/mem0/run-cards/<run-id>.md
```

## Promotion Rules

- Do not promote a mem0 embedding model unless memory add/search and direct embedding benchmarks both improve or tie the current default.
- Do not promote a reranker unless it improves recency conflicts without reducing direct recall or distractor resistance.
- Do not promote an extractor unless JSON validity, transient-noise rejection, and durable fact extraction all pass.
- Keep `nomic-embed-text:latest` and `sam860/LFM2:2.6b` as rollback defaults until a candidate passes the expanded suite.
