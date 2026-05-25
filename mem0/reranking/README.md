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
| `qwen3_causal_lm` / `Qwen/Qwen3-Reranker-0.6B` | 1.000 | 1.000 | 1.000 |

Decision: `score_plus_created_at_rank` remains the best no-download reranker on
the expanded seed suite. `lexical_overlap` is useful as a sanity baseline but
misses one recency conflict.

Learned Qwen3 0.6B reranker:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id rerank-qwen3-0-6b-fixed-20260526
```

The source Hugging Face model uses the same yes/no causal-LM scoring shape as
the public `onnx-community/Qwen3-Reranker-0.6B-ONNX` card. It passed the fixed
6-case suite and both BGE/nomic expanded 12-case derived suites at top-1
`1.000`, recall@3 `1.000`, MRR `1.000`, and nDCG@3 `1.000`. Keep it as the
next learned read-reranker candidate; the ONNX/Transformers.js runtime bridge
still needs separate proof before claiming ONNX local runtime readiness.

BGE-M3 expanded replay:

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_reranking_suite_from_embedding_results.py \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --results /Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-bge-m3-cpu-expanded-20260526/results.jsonl \
  --run-id bge-m3-expanded-derived-reranking-20260526

./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --suite /Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-derived-reranking-20260526/candidate-suite.json \
  --strategy score_plus_created_at_rank_close_margin \
  --recency-weight 0.20 \
  --run-id bge-m3-expanded-close-margin-rerank-20260526
```

| Strategy | Top-1 | Recency conflict | Distractor resistance |
|---|---:|---:|---:|
| `vector` | 0.917 | 0.500 | 1.000 |
| `score_plus_created_at_rank` | 0.917 | 1.000 | 0.750 |
| `lexical_overlap` | 0.917 | 0.500 | 1.000 |
| `score_plus_created_at_rank_close_margin` | 1.000 | 1.000 | 1.000 |
| `qwen3_causal_lm` / `Qwen/Qwen3-Reranker-0.6B` | 1.000 | 1.000 | 1.000 |

Decision: prefer `score_plus_created_at_rank_close_margin` for the next
read-only wrapper test. It keeps recency as a tie-breaker for close semantic
margins instead of letting newer but semantically weaker memories override
older source-grounded facts.

Nomic expanded replay:

| Strategy | Top-1 | Recency conflict | Distractor resistance |
|---|---:|---:|---:|
| `vector` | 0.833 | 0.500 | 1.000 |
| `score_plus_created_at_rank` | 0.750 | 1.000 | 0.750 |
| `lexical_overlap` | 0.917 | 0.500 | 1.000 |
| `score_plus_created_at_rank_close_margin` | 0.917 | 1.000 | 1.000 |
| `qwen3_causal_lm` / `Qwen/Qwen3-Reranker-0.6B` | 1.000 | 1.000 | 1.000 |

The close-margin strategy also improves the default nomic path without touching
`mem0_nomic_768`. It leaves one direct semantic miss (`ollama-retest`) for a
future embedder or learned reranker. The Qwen3 0.6B causal-LM reranker closes
that miss in offline fixed-candidate replay and now has a live read-only wrapper
smoke, but it is not ready to become the default live read path because one-shot
CLI use still pays model load time.

Live read-only wrapper:

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_rerank_search.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --strategy score_plus_created_at_rank_close_margin \
  --recency-weight 0.20
```

This calls `mem0 <tool> search`, reranks the returned JSON locally, and prints JSON. It does not write memories or change `~/.mem0/config.json`.

2026-05-26 blocker, superseded: the wrapper exposed
`score_plus_created_at_rank_close_margin`, but live smoke was blocked until
local Ollama recovered. Historical blocker evidence is recorded in
`reports/benchmark/mem0/mem0-margin-rerank-live-smoke-blocked-20260526.md`.

2026-05-26 update: live read-only wrapper smoke passed after starting Ollama
from `/Volumes/PortableSSD/Ollama/mem0-clean-models` and releasing a stale
Qdrant file lock. Use:

```bash
scripts/start_mem0_ollama.sh
```

Then run the wrapper command above. Evidence is recorded in
`reports/benchmark/mem0/mem0-margin-rerank-live-smoke-20260526.md`.

Qwen3 learned reranker live wrapper:

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

2026-05-26 result: exit code `0`, one returned memory, mem0 search latency
`3.920s`, Qwen3 scoring latency `0.216s`, and one-shot total latency `12.093s`.
Evidence is recorded in
`reports/benchmark/mem0/qwen3-0-6b-live-rerank-smoke-20260526.md`.

Warm Qwen3 helper:

```bash
source scripts/env.sh
./.venv/bin/python scripts/qwen3_reranker_service.py \
  --host 127.0.0.1 \
  --port 8765 \
  --model Qwen/Qwen3-Reranker-0.6B \
  --device auto \
  --local-files-only \
  --quiet
```

Then add `--qwen3-local-files-only --qwen3-server-url http://127.0.0.1:8765`
to the live wrapper command. The first service-backed request still loads the
model, but the second warm request completed in `4.112s` total with Qwen
scoring at `0.119s`. Evidence is recorded in
`reports/benchmark/mem0/qwen3-0-6b-warm-service-rerank-smoke-20260526.md`.

This is not enough to change live mem0 behavior. It proves the failure is addressable after retrieval. The next step is to compare:

- vector-only ordering
- `score_plus_created_at_rank_close_margin`
- a warm-service learned/local reranker such as `Qwen/Qwen3-Reranker-0.6B`
  or `Qwen/Qwen3-Reranker-4B`
- conflict-aware memory update/supersession metadata

Current live-store caveat: on 2026-05-26, broad live probes all returned only
one memory, so a real live multi-result comparison is blocked until there is an
isolated fixture store or captured replay with multiple candidates. Evidence is
recorded in `reports/benchmark/mem0/live-multiretrieval-readiness-20260526.md`.

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
