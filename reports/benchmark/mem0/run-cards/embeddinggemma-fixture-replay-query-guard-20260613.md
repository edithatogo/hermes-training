# mem0 Run Card

Date: 2026-06-13T00:32:42.605519+00:00
Run ID: embeddinggemma-fixture-replay-query-guard-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/embeddinggemma-fixture-replay-query-guard-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | |
| Runtime | query_terms_guarded |
| Endpoint | |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/embeddinggemma-fixture-replay-query-guard-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_rerank_replay.py \
  --strategy query_terms_guarded \
  --fixture-results /Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-embeddinggemma-llamacpp-server-wrapper-20260613/results.jsonl \
  --fixture-source-suite benchmarks/mem0_memory/live_fixture_differentiation_suite.json \
  --fixture-source-strategy vector \
  --run-id embeddinggemma-fixture-replay-query-guard-20260613
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
| Add latency p50 |  |
| Search/embed/extract latency p50 |  |
| Search/embed/extract latency p95 |  |
| Rerank latency p50 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The replay suite passed through the read-only wrapper path; keep it as integration evidence and require live multi-result or isolated-store proof before default promotion.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
