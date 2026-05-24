# mem0 Benchmark Plan

mem0 needs different benchmarks from Hermes chat models. The question is not whether a model writes a good assistant answer; it is whether the memory system stores the right durable facts and retrieves them at the right time.

## Relevant Benchmark Families

| Benchmark family | Use here | Notes |
|---|---|---|
| Memory add/search smoke | Required local gate | Confirms the configured mem0 stack can write and retrieve basic memories. |
| Recency conflict tests | Required local gate | Newer preferences or facts must outrank older conflicting memories. |
| Distractor resistance tests | Required local gate | Similar but irrelevant memories must not displace the target fact. |
| Document-grounded recall | Pilot gate | Uses citation-like fields and checks whether retrieved memories support an answer. |
| MTEB retrieval tasks | Embedding/retriever gate | Use retrieval-focused tasks such as SciFact, NFCorpus, HotpotQA, and ArguAna when practical. |
| BEIR-style retrieval | Embedding/retriever gate | Useful for dense retrievers, rerankers, and late-interaction models. |
| RAGAS-style faithfulness/context metrics | Optional integration gate | Useful after a retriever feeds an answer generator; not a replacement for raw retrieval metrics. |
| LongMemEval / LoCoMo-style memory QA | Watchlist | Useful if a local, license-compatible fixture is adopted. Keep private user data out of published scores. |

The first checked-in suite is `benchmarks/mem0_memory/smoke_suite.json`. It is intentionally tiny and local-safe. Expand it before using scores as quality claims.

## Core Metrics

For mem0 add/search:

- case pass rate
- recall at k
- top-1 expected hit rate
- recency-conflict pass rate
- distractor-resistance pass rate
- add latency p50/p95
- search latency p50/p95
- cleanup success count

For embeddings and retrievers:

- Recall@k
- nDCG@10
- MRR@10
- index build time
- query latency p50/p95
- memory footprint
- collection or index size
- embedding dimension and normalization policy

For extraction models:

- extracted-memory usefulness
- duplicate creation rate
- hallucinated-memory rate
- preference update correctness
- unsafe or secret-like memory rejection
- write latency

## Local Command

Dry-run validation:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py --dry-run
```

Run against the current mem0 CLI:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool cmd \
  --suite benchmarks/mem0_memory/smoke_suite.json \
  --run-id mem0-current-smoke-$(date +%Y%m%d-%H%M%S)
```

The runner prefixes temporary memories with the run id and deletes added memory ids at the end unless `--keep-memories` is provided.

Run a lower-level Ollama embedding retrieval check:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-nomic-smoke-$(date +%Y%m%d-%H%M%S)
```

Use this before changing mem0 collections. It tests whether the embedding model ranks relevant memory documents above close distractors without involving extraction or Qdrant write behavior.

Validate contrastive seed data for future embedding/retriever fine-tunes:

```bash
source scripts/env.sh
./.venv/bin/python scripts/validate_mem0_triplets.py mem0/data/contrastive_seed.jsonl
```

Evaluate offline reranking over a saved mem0 benchmark run:

```bash
source scripts/env.sh
./.venv/bin/python scripts/evaluate_mem0_reranking.py \
  --run-dir /Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524 \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20
```

Use reranking reports to decide whether a failure needs a better embedder, a reranker, or memory-update metadata.

Run an Ollama memory-extraction smoke test:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_memory_extraction_benchmark.py \
  --model 'sam860/LFM2:2.6b' \
  --suite benchmarks/mem0_extraction/smoke_suite.json
```

Extractor scores are separate from embedding scores. A good extractor must produce valid memory JSON, avoid transient noise, and preserve durable project/tool facts.

## Promotion Rule

Do not make a new embedder, extractor, or retriever the default unless:

1. The existing default is still restorable.
2. The candidate uses its own collection or index when dimensions or retrieval shape differ.
3. The smoke suite passes at `1.000`.
4. Recency-conflict and distractor cases pass.
5. p95 search latency remains acceptable for interactive agent use.
6. The run card records exact runtime, model id, collection name, dimensions, and rollback command.
