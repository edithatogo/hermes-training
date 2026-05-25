# mem0 Isolated Live Fixture Multi-Result Rerank

Date: 2026-05-26

## Purpose

Run a real mem0 add/search benchmark against an isolated, non-sensitive fixture
store so rerankers can be compared on live multi-result retrieval without
touching the default `~/.mem0/config.json` or `mem0_nomic_768` collection.

## Isolation

The run used `MEM0_CONFIG_PATH` through
`scripts/run_mem0_isolated_fixture_rerank.py`. The generated config pointed at:

- collection: `mem0_fixture_mem0_live_fixture_qwen3_multiretrieval_rerank_20260526`
- Qdrant path: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526/qdrant`
- history DB: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526/history.db`

The fixture contains only checked-in synthetic benchmark facts from
`benchmarks/mem0_memory/live_fixture_multi_result_suite.json`.

## Command

```bash
source scripts/env.sh

./.venv/bin/python scripts/qwen3_reranker_service.py \
  --host 127.0.0.1 \
  --port 8765 \
  --model Qwen/Qwen3-Reranker-0.6B \
  --device auto \
  --max-length 4096 \
  --local-files-only \
  --quiet

./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --suite benchmarks/mem0_memory/live_fixture_multi_result_suite.json \
  --run-id mem0-live-fixture-qwen3-multiretrieval-rerank-20260526 \
  --qwen3-local-files-only \
  --qwen3-server-url http://127.0.0.1:8765 \
  --keep-fixture
```

## Results

The run added 18 fixture memories across 6 cases. Every query returned multiple
candidates: input count min `3`, max `5`.

| Strategy | Pass | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | Distractor resistance | p50 rerank |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `vector` | 0.667 | 0.667 | 1.000 | 0.833 | 0.877 | 0.500 | 1.000 | 0.000s |
| `score_plus_created_at_rank_close_margin` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000s |
| `qwen3_causal_lm` / `Qwen/Qwen3-Reranker-0.6B` warm service | 0.667 | 0.667 | 1.000 | 0.833 | 0.877 | 0.500 | 1.000 | 0.491s |

Latency:

- add p50: `2.883s`; add p95: `3.524s`
- search p50: `2.886s`; search p95: `2.920s`
- warm Qwen3 rerank p50: `0.491s`; p95: `0.645s`

Raw output:

`/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526`

## Decision

Do not promote Qwen3 0.6B as the live mem0 reranker from this fixture. It
matched vector ordering and failed one recency-conflict lane that the
close-margin heuristic fixed.

Promote the next development focus to the no-download
`score_plus_created_at_rank_close_margin` wrapper path. It passed the isolated
live add/search multi-result fixture at `1.000` without changing defaults and
with negligible rerank latency.

Keep Qwen3 0.6B as a learned reranker candidate for semantic misses, but it
needs prompt/metadata work before another live recency fixture gate.
