# mem0 Multi-Result Rerank Replay Comparison

Date: 2026-05-26

## Purpose

Compare the no-download close-margin heuristic with the warm
`Qwen/Qwen3-Reranker-0.6B` service path on multi-result candidate suites without
writing to the live default mem0 store.

The live default store currently returns singleton results, so this replay
harness uses captured fixed and expanded candidate suites while routing ranking
through the same read-only wrapper abstraction as live mem0 reads.

## Commands

Heuristic replay:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_rerank_replay.py \
  --strategy score_plus_created_at_rank_close_margin \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id mem0-replay-close-margin-fixed-20260526
```

Warm Qwen3 replay:

```bash
source scripts/env.sh
./.venv/bin/python scripts/qwen3_reranker_service.py \
  --host 127.0.0.1 \
  --port 8765 \
  --model Qwen/Qwen3-Reranker-0.6B \
  --device auto \
  --local-files-only \
  --quiet

./.venv/bin/python scripts/run_mem0_rerank_replay.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --qwen3-local-files-only \
  --qwen3-server-url http://127.0.0.1:8765 \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id mem0-replay-qwen3-06b-warm-fixed-20260526
```

The same commands were repeated for the BGE-derived and nomic-derived expanded
candidate suites under `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark`.

## Results

| Suite | Strategy | Cases | Top-1 | Recall@3 | MRR | nDCG@3 | Recency | Distractor | p50 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fixed | close-margin heuristic | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000s |
| Fixed | warm Qwen3 0.6B | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.220s |
| BGE-derived expanded | close-margin heuristic | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000s |
| BGE-derived expanded | warm Qwen3 0.6B | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.281s |
| Nomic-derived expanded | close-margin heuristic | 12 | 0.917 | 1.000 | 0.958 | 0.969 | 1.000 | 1.000 | 0.000s |
| Nomic-derived expanded | warm Qwen3 0.6B | 12 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.250s |

## Decision

Keep the close-margin heuristic as the default no-download comparison baseline.
It is effectively free and passed fixed plus BGE-derived replay. Use warm Qwen3
0.6B as the stronger candidate when semantic misses matter: it closed the
nomic-derived miss while keeping all recency and distractor gates at `1.000`.

Do not promote either path to a default live integration from replay alone. The
next promotion gate is an isolated non-sensitive mem0 fixture store or a live
store with genuine multi-result searches.
