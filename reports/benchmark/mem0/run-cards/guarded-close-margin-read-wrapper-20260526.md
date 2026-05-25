# mem0 Run Card

Date: 2026-05-25T17:33:54.767587+00:00
Run ID: guarded-close-margin-read-wrapper-20260526
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/guarded-close-margin-read-wrapper-20260526/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | `cmd` |
| Runtime | score_plus_created_at_rank_close_margin |
| Endpoint | |
| Collection or index | `mem0_fixture_guarded_close_margin_read_wrapper_20260526` |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/guarded-close-margin-read-wrapper-20260526` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --suite benchmarks/mem0_memory/live_fixture_multi_result_suite.json \
  --run-id guarded-close-margin-read-wrapper-20260526
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 1.000 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 1.000 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 1.000 |
| JSON validity rate |  |
| Add latency p50 | 2.886 |
| Search/embed/extract latency p50 | 2.890 |
| Search/embed/extract latency p95 | 2.910 |
| Rerank latency p50 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The isolated fixture passed the live add/search multi-result gate without touching defaults; require a deliberate default-integration plan before promotion.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
