# mem0 Run Card

Date: 2026-06-12T13:33:40.972036+00:00
Run ID: retriever-lfm2-colbert-expanded-20260612
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-retriever-benchmark/retriever-lfm2-colbert-expanded-20260612/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | retriever |
| Model/tool | `LiquidAI/LFM2-ColBERT-350M` |
| Runtime | retriever-service (mps) |
| Endpoint | `http://127.0.0.1:8765` |
| Collection or index | `mem0_lfm2_colbert_350m` |
| Embedding dims |  |
| Distance metric | MaxSim / late-interaction |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-retriever-benchmark/retriever-lfm2-colbert-expanded-20260612` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_retriever_service_benchmark.py \
  --base-url http://127.0.0.1:8765 \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --run-id retriever-lfm2-colbert-expanded-20260612
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.917 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.917 |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 0.238 |
| Search/embed/extract latency p95 | 0.497 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The retriever service did not reach the strict smoke gate and should remain a candidate.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
