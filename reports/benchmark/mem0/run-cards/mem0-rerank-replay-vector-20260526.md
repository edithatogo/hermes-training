# mem0 Run Card

Date: 2026-05-25T17:10:10.012428+00:00
Run ID: mem0-rerank-replay-vector-20260526
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/mem0-rerank-replay-vector-20260526/summary.json`

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
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/mem0-rerank-replay-vector-20260526` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_rerank_replay.py \
  --strategy vector \
  --suite /Volumes/PortableSSD/GitHub/hermes-training/benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id mem0-rerank-replay-vector-20260526
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.667 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.667 |
| Recency conflict pass rate | 0.000 |
| Distractor resistance pass rate | 1.000 |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 |  |
| Search/embed/extract latency p95 |  |
| Rerank latency p50 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The replay suite did not reach the strict 1.000 top-1 gate and should remain a comparison baseline.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
