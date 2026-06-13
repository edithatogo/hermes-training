# mem0 Run Card

Date: 2026-05-25T18:02:53.235711+00:00
Run ID: qwen3-0-6b-onnx-transformersjs-bridge-20260526
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/qwen3-0-6b-onnx-transformersjs-bridge-20260526/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | `onnx-community/Qwen3-Reranker-0.6B-ONNX` |
| Runtime |  |
| Endpoint | |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/qwen3-0-6b-onnx-transformersjs-bridge-20260526` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy <strategy> \
  --model onnx-community/Qwen3-Reranker-0.6B-ONNX \
  --suite /Volumes/PortableSSD/GitHub/hermes-training/benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id qwen3-0-6b-onnx-transformersjs-bridge-20260526
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.000 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 0.000 |
| Top-1 expected rate | 0.000 |
| Recency conflict pass rate | 0.000 |
| Distractor resistance pass rate | 0.000 |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 |  |
| Search/embed/extract latency p95 |  |
| Rerank latency p50 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: This reranker did not reach the strict fixed-suite gate and should remain a comparison baseline.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
