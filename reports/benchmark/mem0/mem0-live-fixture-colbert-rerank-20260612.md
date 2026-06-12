# mem0 Live Fixture ColBERT Rerank - 2026-06-12

## Scope

This run verifies `LiquidAI/LFM2-ColBERT-350M` on a real mem0 add/search
fixture with multi-result candidate sets. The harness used an output-local
`MEM0_CONFIG_PATH`, an output-local Qdrant path, and did not edit
`~/.mem0/config.json` or the default `mem0_nomic_768` collection.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/lfm2_colbert_service.py \
  --host 127.0.0.1 \
  --port 8765 \
  --model LiquidAI/LFM2-ColBERT-350M \
  --device auto \
  --local-files-only \
  --quiet

source scripts/env.sh
./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --suite benchmarks/mem0_memory/live_fixture_multi_result_suite.json \
  --run-id mem0-live-fixture-colbert-rerank-20260612 \
  --include-colbert \
  --skip-qwen3 \
  --timeout-s 120 \
  --retriever-timeout-s 120
```

## Result

| Strategy | Pass | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | p50 rerank |
|---|---:|---:|---:|---:|---:|---:|---:|
| `vector` | 0.667 | 0.667 | 1.000 | 0.833 | 0.877 | 0.500 | 0.000s |
| `score_plus_created_at_rank_close_margin` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000s |
| `retriever_service` | 0.833 | 0.833 | 1.000 | 0.917 | 0.938 | 0.500 | 0.288s |

Fixture search returned `3` to `5` candidates per query across six cases.
ColBERT improved over raw vector ordering, but missed the current-vs-old
embedder recency conflict. The close-margin heuristic remains the best live
mem0 read path for this fixture.

Raw output:
`/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-colbert-rerank-20260612`

## Decision

`LiquidAI/LFM2-ColBERT-350M` has now completed a multi-result mem0 fixture
benchmark. It should remain an opt-in research path rather than the Hermes
mem0 default because it does not beat the current close-margin guarded read
path on recency-sensitive local memory.
