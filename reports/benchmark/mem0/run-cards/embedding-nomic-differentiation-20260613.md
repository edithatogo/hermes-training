# mem0 Run Card

Date: 2026-06-12T14:21:39.001202+00:00
Run ID: embedding-nomic-differentiation-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-differentiation-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | embedder |
| Model/tool | `nomic-embed-text:latest` |
| Runtime | openai-compatible |
| Endpoint | `http://127.0.0.1:11434` |
| Collection or index | |
| Embedding dims | 768 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-differentiation-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_differentiation_suite.json \
  --run-id embedding-nomic-differentiation-20260613
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.600 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 0.800 |
| Top-1 expected rate | 0.600 |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 0.019 |
| Search/embed/extract latency p95 | 0.041 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The endpoint path is proven, but the embedding model still needs a recency or reranking fix before promotion beyond the current default.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
