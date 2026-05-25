# Nomic Expanded Retrieval and Reranker Replay

Date: 2026-05-26

## Purpose

Run the expanded mem0 retrieval gate for the current rollback embedder,
`nomic-embed-text:latest`, now that the clean SSD-backed Ollama root is
responsive. This is the direct comparison requested after the BGE-M3 expanded
run.

## Runtime

- Ollama root: `/Volumes/PortableSSD/Ollama/mem0-clean-models`
- Models visible: `nomic-embed-text:latest`, `sam860/LFM2:2.6b`
- Benchmark output root: `/Volumes/PortableSSD/hermes-evals`
- No change made to `~/.mem0/config.json` or `mem0_nomic_768`.

## Dense Retrieval

Command:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --model nomic-embed-text:latest \
  --base-url http://127.0.0.1:11434 \
  --run-id embedding-nomic-expanded-20260526
```

Output:

```text
/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-expanded-20260526
```

| Metric | Value |
|---|---:|
| Cases | 12 |
| Top-1 accuracy | 0.833 |
| Recall@3 | 1.000 |
| MRR | 0.917 |
| nDCG@3 | 0.938 |
| Embedding dims | 768 |
| Embed latency p50 | 0.021s |
| Embed latency p95 | 0.087s |

Dense retrieval misses:

- `recency-preference`: ranks the older preference above the current preference.
- `ollama-retest`: ranks the LM Studio validation note above the desired
  retest-after-upgrade note.

## Nomic-Derived Reranker Replay

The nomic ranked output was converted into the fixed reranking format:

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_reranking_suite_from_embedding_results.py \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --results /Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-expanded-20260526/results.jsonl \
  --run-id nomic-expanded-derived-reranking-20260526
```

Derived suite:

```text
/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-derived-reranking-20260526/candidate-suite.json
```

| Strategy | Top-1 | Recall@3 | Recency conflict | Distractor resistance | Output |
|---|---:|---:|---:|---:|---|
| `vector` | 0.833 | 1.000 | 0.500 | 1.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-vector-rerank-20260526` |
| `score_plus_created_at_rank` | 0.750 | 1.000 | 1.000 | 0.750 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-created-at-rank-20260526` |
| `lexical_overlap` | 0.917 | 1.000 | 0.500 | 1.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-lexical-rerank-20260526` |
| `score_plus_created_at_rank_close_margin` | 0.917 | 1.000 | 1.000 | 1.000 | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-close-margin-rerank-20260526` |

The margin-gated recency strategy fixed the recency conflict without the older
`score_plus_created_at_rank` distractor regression. It still misses
`ollama-retest`, which is a semantic retrieval/ranking weakness rather than a
recency conflict.

## BGE-M3 Comparison

| Model / strategy | Top-1 | Recall@3 | p50 latency | Decision |
|---|---:|---:|---:|---|
| `nomic-embed-text:latest` dense | 0.833 | 1.000 | 0.021s | keep as default rollback |
| `nomic` + close-margin rerank | 0.917 | 1.000 | ~0.000s rerank | validated read-path improvement, not default mutation |
| `BAAI/bge-m3` dense CPU | 0.917 | 1.000 | 0.097s | stronger dense candidate, not promoted |
| `BAAI/bge-m3` + close-margin rerank | 1.000 | 1.000 | ~0.000s rerank | strongest offline result so far |

## Decision

Keep `nomic-embed-text:latest` as the live default because it is already the
working 768-dimensional collection, fast, and recall-complete on this suite.
Use `score_plus_created_at_rank_close_margin` as the best validated read-only
wrapper strategy while preparing learned/local reranker comparisons.

Do not migrate `mem0_nomic_768` to BGE-M3 from this evidence alone. BGE-M3 is
stronger on dense top-1, but requires a separate 1024-dimensional collection and
still benefits from reranking.
