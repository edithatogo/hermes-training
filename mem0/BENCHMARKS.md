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

## Benchmark Index

Generate the current mem0 benchmark index:

```bash
source scripts/env.sh
./.venv/bin/python scripts/summarize_mem0_benchmarks.py \
  /Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/*/summary.json \
  /Volumes/PortableSSD/hermes-evals/embedding-benchmark/*/summary.json \
  /Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/*/summary.json \
  --output reports/benchmark/mem0/index.md
```

Generate a run card from any saved mem0 benchmark summary:

```bash
source scripts/env.sh
./.venv/bin/python scripts/create_mem0_run_card.py \
  /Volumes/PortableSSD/hermes-evals/<benchmark-kind>/<run-id>/summary.json \
  --output reports/benchmark/mem0/run-cards/<run-id>.md
```

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

Run the expanded recency suite:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool cmd \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --rerank-strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id mem0-current-nomic-recency-reranked-$(date +%Y%m%d-%H%M%S)
```

Run a lower-level Ollama embedding retrieval check:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-nomic-smoke-$(date +%Y%m%d-%H%M%S)
```

Use this before changing mem0 collections. It tests whether the embedding model ranks relevant memory documents above close distractors without involving extraction or Qdrant write behavior.

Run the same embedding suite through an OpenAI-compatible endpoint:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_embedding_benchmark.py \
  --base-url http://127.0.0.1:11434/v1 \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-nomic-openai-$(date +%Y%m%d-%H%M%S)
```

Use this path for LM Studio, `llama-server`, Ollama `/v1`, and any other local server that presents OpenAI-compatible embeddings.

Run a local `sentence-transformers` embedding candidate:

```bash
source scripts/env.sh
python -m pip install -r requirements-mem0-embeddings.txt
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model BAAI/bge-m3 \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-bge-m3-$(date +%Y%m%d-%H%M%S)
```

This optional path is for BGE-M3, Jina, Qwen embedding, and other Hugging Face
retrieval candidates that are not already available through Ollama, LM Studio,
or `llama-server`.

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

Run fixed-candidate reranking baselines before testing a learned reranker:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy vector \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json

./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json
```

For a CrossEncoder-style reranker such as `Qwen/Qwen3-Reranker-4B`, install the
optional reranker deps first and use:

```bash
source scripts/env.sh
python -m pip install -r requirements-mem0-rerankers.txt
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy cross_encoder \
  --model Qwen/Qwen3-Reranker-4B \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json
```

For Qwen3 rerankers that score yes/no logits from a causal LM, use the
dedicated scorer:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json
```

Current expanded fixed-suite reranker scores:

| Strategy | Top-1 | Recency conflict | Distractor resistance |
|---|---:|---:|---:|
| `vector` | 0.667 | 0.000 | 1.000 |
| `score_plus_created_at_rank` | 1.000 | 1.000 | 1.000 |
| `lexical_overlap` | 0.833 | 0.500 | 1.000 |
| `qwen3_causal_lm` / `Qwen/Qwen3-Reranker-0.6B` | 1.000 | 1.000 | 1.000 |

Current expanded embedding-derived reranker scores:

| Source | Strategy | Top-1 | Recency conflict | Distractor resistance |
|---|---|---:|---:|---:|
| BGE-M3 | `vector` | 0.917 | 0.500 | 1.000 |
| BGE-M3 | `score_plus_created_at_rank_close_margin` | 1.000 | 1.000 | 1.000 |
| BGE-M3 | `qwen3_causal_lm` / `Qwen/Qwen3-Reranker-0.6B` | 1.000 | 1.000 | 1.000 |
| nomic | `vector` | 0.833 | 0.500 | 1.000 |
| nomic | `score_plus_created_at_rank_close_margin` | 0.917 | 1.000 | 1.000 |
| nomic | `qwen3_causal_lm` / `Qwen/Qwen3-Reranker-0.6B` | 1.000 | 1.000 | 1.000 |

Run a read-only reranked search against the live mem0 store:

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20
```

Run the learned Qwen3 0.6B reranker against the same live mem0 search output:

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --qwen3-local-files-only \
  --timeout-s 120
```

2026-05-26 live smoke: exit code `0`, one returned memory, mem0 search latency
`3.920s`, Qwen3 scoring latency `0.216s`, one-shot total latency `12.093s`.
Keep this as a candidate wrapper until a warm local service removes repeated
model-load overhead.

Run the warm service path:

```bash
source scripts/env.sh
./.venv/bin/python scripts/qwen3_reranker_service.py \
  --host 127.0.0.1 \
  --port 8765 \
  --model Qwen/Qwen3-Reranker-0.6B \
  --device auto \
  --local-files-only \
  --quiet

./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --qwen3-local-files-only \
  --qwen3-server-url http://127.0.0.1:8765 \
  --timeout-s 120
```

2026-05-26 warm-service smoke: the second service-backed request completed in
`4.112s` total with Qwen scoring latency `0.119s`; mem0 search accounted for
`3.979s`.

Run multi-result replay through the live-wrapper abstraction without writing to
the live mem0 store:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_rerank_replay.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --qwen3-local-files-only \
  --qwen3-server-url http://127.0.0.1:8765 \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json
```

Current replay comparison:

| Suite | Close-margin top-1 | Warm Qwen3 top-1 | Warm Qwen3 p50 |
|---|---:|---:|---:|
| Fixed | 1.000 | 1.000 | 0.220s |
| BGE-derived expanded | 1.000 | 1.000 | 0.281s |
| Nomic-derived expanded | 0.917 | 1.000 | 0.250s |

Run an Ollama memory-extraction smoke test:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_memory_extraction_benchmark.py \
  --model 'sam860/LFM2:2.6b' \
  --suite benchmarks/mem0_extraction/smoke_suite.json
```

Extractor scores are separate from embedding scores. A good extractor must produce valid memory JSON, avoid transient noise, and preserve durable project/tool facts.

Current expanded extraction scores:

| Model | Pass | JSON valid | Forbidden hit | Empty-case pass |
|---|---:|---:|---:|---:|
| `sam860/LFM2:2.6b` with `mem0/extraction/system_prompt.md` | 1.000 | 1.000 | 0.000 | 1.000 |
| `hermes3:8b` | 0.571 | 0.714 | 0.143 | 0.857 |

The extraction benchmark uses an OpenAI-compatible chat-completions endpoint.
For non-Ollama servers, use the generic wrapper and set `--base-url`:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --base-url http://127.0.0.1:1234/v1 \
  --model local-model-id \
  --suite benchmarks/mem0_extraction/smoke_suite.json
```

## Promotion Rule

Do not make a new embedder, extractor, or retriever the default unless:

1. The existing default is still restorable.
2. The candidate uses its own collection or index when dimensions or retrieval shape differ.
3. The smoke suite passes at `1.000`.
4. Recency-conflict and distractor cases pass.
5. p95 search latency remains acceptable for interactive agent use.
6. The run card records exact runtime, model id, collection name, dimensions, and rollback command.
