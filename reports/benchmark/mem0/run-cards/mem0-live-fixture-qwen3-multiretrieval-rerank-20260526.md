# mem0 Run Card

Date: 2026-05-25T17:23:04.295646+00:00
Run ID: mem0-live-fixture-qwen3-multiretrieval-rerank-20260526
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | `Qwen/Qwen3-Reranker-0.6B` |
| Runtime | qwen3_causal_lm:Qwen/Qwen3-Reranker-0.6B |
| Endpoint | |
| Collection or index | `mem0_fixture_mem0_live_fixture_qwen3_multiretrieval_rerank_20260526` |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --qwen3-model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-local-files-only \
  --qwen3-server-url http://127.0.0.1:8765 \
  --keep-fixture \
  --suite benchmarks/mem0_memory/live_fixture_multi_result_suite.json \
  --run-id mem0-live-fixture-qwen3-multiretrieval-rerank-20260526
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.667 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.667 |
| Recency conflict pass rate | 0.500 |
| Distractor resistance pass rate | 1.000 |
| JSON validity rate |  |
| Add latency p50 | 2.883 |
| Search/embed/extract latency p50 | 2.886 |
| Search/embed/extract latency p95 | 2.920 |
| Rerank latency p50 | 0.491 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The isolated fixture did not prove strict multi-result top-1 behavior and should remain a comparison baseline.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
