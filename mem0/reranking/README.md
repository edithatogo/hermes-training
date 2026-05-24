# mem0 Reranking

Reranking sits between vector search and the final memories shown to an agent.

The current `nomic-embed-text` baseline retrieves the relevant current preference in the recency case, but ranks the older conflicting preference first. That means the first fix does not need to replace embeddings immediately; a post-ranker can be tested independently.

## Current Prototype

Offline evaluator:

```bash
source scripts/env.sh
./.venv/bin/python scripts/evaluate_mem0_reranking.py \
  --run-dir /Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524 \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id created-at-rank-020-20260524
```

Result on the first seed suite: `1.000` pass rate.

The expanded recency suite is:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool cmd \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --rerank-strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id mem0-current-nomic-recency-reranked-20260524
```

Baseline result: `0.400` pass rate. Reranked result: `1.000` pass rate.

Fixed candidate reranking suite:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy vector \
  --run-id fixed-rerank-vector-20260524

./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20 \
  --run-id fixed-rerank-created-at-rank-20260524
```

Expanded fixed-suite results:

| Strategy | Top-1 | Recency conflict | Distractor resistance |
|---|---:|---:|---:|
| `vector` | 0.667 | 0.000 | 1.000 |
| `score_plus_created_at_rank` | 1.000 | 1.000 | 1.000 |
| `lexical_overlap` | 0.833 | 0.500 | 1.000 |

Decision: `score_plus_created_at_rank` remains the best no-download reranker on
the expanded seed suite. `lexical_overlap` is useful as a sanity baseline but
misses one recency conflict.

Live read-only wrapper:

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy score_plus_created_at_rank \
  --recency-weight 0.20
```

This calls `mem0 <tool> search`, reranks the returned JSON locally, and prints JSON. It does not write memories or change `~/.mem0/config.json`.

This is not enough to change live mem0 behavior. It proves the failure is addressable after retrieval. The next step is to expand the suite and compare:

- vector-only ordering
- `score_plus_created_at_rank`
- a learned/local reranker such as `Qwen/Qwen3-Reranker-4B`
- conflict-aware memory update/supersession metadata

Optional reranker dependencies are intentionally separate from the base repo
environment:

```bash
source scripts/env.sh
python -m pip install -r requirements-mem0-rerankers.txt
```

`FlagEmbedding` pulls extra retrieval-evaluation packages and source builds, so
install it only when testing BGE-specific reranking or training paths.

## Integration Rule

A reranker must not hide relevant older facts just because they are old. Recency should help with preference updates and conflicts, but source-grounded facts still need semantic relevance to dominate.
