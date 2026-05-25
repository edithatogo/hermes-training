# mem0 Namespace Fixture Rerank Comparison

Date: 2026-05-26

## Purpose

Validate reranking against real `mem0 add/search` behavior without writing test
memories into the default `cmd` namespace. The fixture used the dedicated
`hermes_fixture` tool namespace and cleanup was left enabled.

This is weaker isolation than the later `MEM0_CONFIG_PATH` fixture because it
still used the default mem0 config and collection. Treat this as historical
namespace-scoped evidence; the stronger config-isolated gate is recorded in
`reports/benchmark/mem0/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526.md`.

## Commands

Close-margin heuristic:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool hermes_fixture \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --rerank-strategy score_plus_created_at_rank_close_margin \
  --run-id mem0-fixture-close-margin-recency-20260526 \
  --timeout-s 180
```

Warm Qwen3 0.6B:

```bash
source scripts/env.sh
./.venv/bin/python scripts/qwen3_reranker_service.py \
  --host 127.0.0.1 \
  --port 8765 \
  --model Qwen/Qwen3-Reranker-0.6B \
  --device auto \
  --local-files-only \
  --quiet

./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool hermes_fixture \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --rerank-strategy qwen3_causal_lm \
  --rerank-model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --qwen3-local-files-only \
  --qwen3-server-url http://127.0.0.1:8765 \
  --run-id mem0-fixture-qwen3-06b-recency-20260526 \
  --timeout-s 180
```

## Results

| Path | Cases | Raw pass | Raw recall@k | Raw top-1 | Rerank pass | Rerank top-1 | Rerank recency | Rerank distractor | Rerank p50 | Cleanup |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Close-margin heuristic | 5 | 0.400 | 1.000 | 0.400 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000s | 11/11 |
| Warm Qwen3 0.6B | 5 | 0.400 | 1.000 | 0.400 | 1.000 | 1.000 | 1.000 | 1.000 | 0.495s | 11/11 |

## Decision

The namespace fixture proves the reranker layer fixes real mem0 add/search
ordering failures without changing the live default `cmd` memory namespace.
Raw retrieval placed the expected fact in the candidate set every time but only
ranked the expected top result correctly in `0.400` of cases. Both rerankers
raised the fixture suite to `1.000`.

Keep `score_plus_created_at_rank_close_margin` as the no-download default
candidate for fixture/live wrapper use. Keep warm Qwen3 0.6B as the stronger
semantic reranker candidate, especially when the nomic-derived replay miss
matters. Do not change the global mem0 config from this alone. Prefer the
stronger config-isolated fixture result for promotion decisions.
