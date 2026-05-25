# mem0 Run Card

Date: 2026-05-25T18:56:04.359220+00:00
Run ID: rerank-flaglow-baai-bge-reranker-v2-m3-mlx-mxfp8-8bit-pairtok-nomic-expanded-20260526
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/rerank-flaglow-baai-bge-reranker-v2-m3-mlx-mxfp8-8bit-pairtok-nomic-expanded-20260526/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | `flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` |
| Runtime | mlx_cross_encoder |
| Endpoint | |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/rerank-flaglow-baai-bge-reranker-v2-m3-mlx-mxfp8-8bit-pairtok-nomic-expanded-20260526` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy mlx_cross_encoder \
  --model flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit \
  --mlx-max-length 1024 \
  --suite /Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/nomic-expanded-derived-reranking-20260526/candidate-suite.json \
  --run-id rerank-flaglow-baai-bge-reranker-v2-m3-mlx-mxfp8-8bit-pairtok-nomic-expanded-20260526
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
| Rerank latency p50 | 0.091 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The fixed suite passed, but learned and heuristic rerankers need a larger suite before live default integration.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
