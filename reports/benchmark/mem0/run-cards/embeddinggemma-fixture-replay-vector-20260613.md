# mem0 Run Card

Date: 2026-06-13T00:32:42.508091+00:00
Run ID: embeddinggemma-fixture-replay-vector-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/embeddinggemma-fixture-replay-vector-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | |
| Runtime | vector |
| Endpoint | |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/embeddinggemma-fixture-replay-vector-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_rerank_replay.py \
  --strategy vector \
  --fixture-results /Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-embeddinggemma-llamacpp-server-wrapper-20260613/results.jsonl \
  --fixture-source-suite benchmarks/mem0_memory/live_fixture_differentiation_suite.json \
  --fixture-source-strategy vector \
  --run-id embeddinggemma-fixture-replay-vector-20260613
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.909 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.909 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 0.750 |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 |  |
| Search/embed/extract latency p95 |  |
| Rerank latency p50 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The replay suite did not reach the strict 1.000 top-1 gate and should remain a comparison baseline.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
