# mem0 Run Card

Date: 2026-05-25T18:58:27.200713+00:00
Run ID: mem0-live-fixture-mlx-bge-reranker-v2-m3-8bit-20260526
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-mlx-bge-reranker-v2-m3-8bit-20260526/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | `flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` |
| Runtime | mlx_cross_encoder:flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit |
| Endpoint | |
| Collection or index | `mem0_fixture_mem0_live_fixture_mlx_bge_reranker_v2_m3_8bit_20260526` |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-mlx-bge-reranker-v2-m3-8bit-20260526` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --mlx-model flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit \
  --mlx-max-length 1024 \
  --keep-fixture \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --run-id mem0-live-fixture-mlx-bge-reranker-v2-m3-8bit-20260526
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
| Add latency p50 | 2.936 |
| Search/embed/extract latency p50 | 2.881 |
| Search/embed/extract latency p95 | 2.898 |
| Rerank latency p50 | 0.145 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The isolated fixture did not prove strict multi-result top-1 behavior and should remain a comparison baseline.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
