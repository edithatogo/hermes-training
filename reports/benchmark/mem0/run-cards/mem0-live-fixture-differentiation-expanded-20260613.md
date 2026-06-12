# mem0 Run Card

Date: 2026-06-12T23:47:37.176735+00:00
Run ID: mem0-live-fixture-differentiation-expanded-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-differentiation-expanded-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | `cmd` |
| Runtime | vector |
| Endpoint | |
| Collection or index | `mem0_fixture_mem0_live_fixture_differentiation_expanded_20260613` |
| Embedding dims | 768 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-differentiation-expanded-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --skip-qwen3 \
  --suite benchmarks/mem0_memory/live_fixture_differentiation_suite.json \
  --run-id mem0-live-fixture-differentiation-expanded-20260613
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.818 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 0.909 |
| Top-1 expected rate | 0.818 |
| Recency conflict pass rate | 0.500 |
| Distractor resistance pass rate | 0.750 |
| JSON validity rate |  |
| Add latency p50 | 2.931 |
| Search/embed/extract latency p50 | 2.935 |
| Search/embed/extract latency p95 | 2.958 |
| Rerank latency p50 | 0.000 |

## Strategy Comparison

| Strategy | Pass | Top-1 | Recall@3 | MRR | nDCG@3 | p50 rerank |
|---|---:|---:|---:|---:|---:|---:|
| `vector` | 0.818 | 0.818 | 0.909 | 0.848 | 0.864 | 0.000 |
| `score_plus_created_at_rank_close_margin` | 0.636 | 0.636 | 0.909 | 0.742 | 0.785 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The isolated fixture did not prove strict multi-result top-1 behavior and should remain a comparison baseline.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
