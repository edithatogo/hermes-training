# BGE-M3 Expanded Retrieval Benchmark

Date: 2026-05-26

## Purpose

The original BGE-M3 smoke suite had only three cases. This run expands the
mem0-oriented retrieval gate to cover direct recall, recency conflict,
distractor resistance, storage policy, runtime status, Azure quota status, and
publication gates before any live collection migration.

## Suite

- Fixture: `benchmarks/embeddings/memory_retrieval_expanded_suite.json`
- Cases: 12
- Categories: `direct_recall`, `recency_conflict`, `distractor_resistance`
- Benchmark output root: `/Volumes/PortableSSD/hermes-evals`

## BGE-M3 Dense Retrieval

Command:

```bash
source scripts/env.sh
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python \
  scripts/run_sentence_transformers_embedding_benchmark.py \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --model BAAI/bge-m3 \
  --device cpu \
  --run-id embedding-bge-m3-cpu-expanded-20260526 \
  --force-exit-after-write
```

Output:

```text
/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-cpu-expanded-20260526
```

| Metric | Value |
|---|---:|
| Cases | 12 |
| Top-1 accuracy | 0.917 |
| Recall@3 | 1.000 |
| MRR | 0.958 |
| nDCG@3 | 0.969 |
| Embedding dims | 1024 |
| Embed latency p50 | 0.097s |
| Embed latency p95 | 0.107s |

The only dense retrieval miss remains `recency-preference`: BGE-M3 ranks the
older preference above the current preference.

## BGE-Derived Reranker Replay

The BGE-M3 ranked output was converted into the fixed reranking format:

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_reranking_suite_from_embedding_results.py \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --results /Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-cpu-expanded-20260526/results.jsonl \
  --run-id bge-m3-expanded-derived-reranking-20260526
```

Derived suite:

```text
/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-derived-reranking-20260526/candidate-suite.json
```

| Strategy | Top-1 | Recall@3 | Recency conflict | Distractor resistance | Output |
|---|---:|---:|---:|---:|---|
| `vector` | 0.917 | 1.000 | 0.500 | 1.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-vector-rerank-20260526` |
| `score_plus_created_at_rank` | 0.917 | 1.000 | 1.000 | 0.750 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-created-at-rank-20260526` |
| `lexical_overlap` | 0.917 | 1.000 | 0.500 | 1.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-lexical-rerank-20260526` |
| `score_plus_created_at_rank_close_margin` | 1.000 | 1.000 | 1.000 | 1.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-close-margin-rerank-20260526` |

The older `score_plus_created_at_rank` heuristic fixed recency but over-promoted
a newer distractor in `semantic-margin-beats-recency`. The new
`score_plus_created_at_rank_close_margin` strategy only applies recency boost
inside a close semantic margin, which preserved source-grounded older facts.

## Nomic Comparison

The current nomic baseline remains the working default. Fresh nomic expanded
re-run was not completed in this slice because local Ollama did not respond to
`ollama list` within 5 seconds while the daemon was running. Existing nomic
smoke evidence remains available in:

- `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-smoke-20260524`
- `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-openai-ollama-smoke-20260524`

## Decision

Do not promote BGE-M3 as the default embedder yet. Promote the margin-gated
reranking strategy to the next live read-only wrapper candidate instead:

- BGE-M3 dense retrieval is strong on the expanded suite but still misses the
  current preference case without reranking.
- The margin-gated recency reranker reaches 1.000 on the BGE-derived expanded
  suite without the large-margin distractor regression.
- A fresh nomic expanded comparison should be run after Ollama responsiveness is
  restored, then the same derived-reranker replay should be applied to nomic.

