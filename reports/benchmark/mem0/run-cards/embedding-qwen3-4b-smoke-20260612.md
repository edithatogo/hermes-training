# mem0 Run Card

Date: 2026-06-12T12:14:08.430083+00:00
Run ID: embedding-qwen3-4b-smoke-20260612
Summary: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-qwen3-4b-smoke-20260612/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | embedder |
| Model/tool | `Qwen/Qwen3-Embedding-4B` |
| Runtime | sentence-transformers |
| Endpoint | |
| Collection or index | |
| Embedding dims | 2560 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-qwen3-4b-smoke-20260612` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model Qwen/Qwen3-Embedding-4B \
  --device cpu \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-qwen3-4b-smoke-20260612
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 1.000 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 1.000 |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 2.155 |
| Search/embed/extract latency p95 | 11.578 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The endpoint path is proven, but the embedding model still needs a recency or reranking fix before promotion beyond the current default.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
