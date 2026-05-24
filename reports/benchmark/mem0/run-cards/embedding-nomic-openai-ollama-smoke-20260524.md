# mem0 Run Card

Date: 2026-05-24T07:14:39.540767+00:00
Run ID: embedding-nomic-openai-ollama-smoke-20260524
Summary: `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-openai-ollama-smoke-20260524/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | embedder |
| Model/tool | `nomic-embed-text:latest` |
| Runtime | openai-compatible-embeddings |
| Endpoint | `http://127.0.0.1:11434/v1` |
| Collection or index | |
| Embedding dims | 768 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-openai-ollama-smoke-20260524` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_embedding_benchmark.py \
  --model nomic-embed-text:latest \
  --base-url http://127.0.0.1:11434/v1 \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-nomic-openai-ollama-smoke-20260524
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.667 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.667 |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 0.025 |
| Search/embed/extract latency p95 | 0.048 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The endpoint path is proven, but the embedding model still needs a recency or reranking fix before promotion beyond the current default.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
