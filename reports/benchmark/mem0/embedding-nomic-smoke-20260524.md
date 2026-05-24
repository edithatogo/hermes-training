# Ollama Embedding Benchmark: nomic-embed-text

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_embedding_benchmark.py \
  --model nomic-embed-text:latest \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-nomic-smoke-20260524
```

## Runtime

| Component | Value |
|---|---|
| Runtime | Ollama |
| Endpoint | `http://127.0.0.1:11434/api/embeddings` |
| Model | `nomic-embed-text:latest` |
| Embedding dims | 768 |

## Result

| Metric | Score |
|---|---:|
| Cases | 3 |
| Top-1 accuracy | 0.667 |
| Recall@3 | 1.000 |
| MRR | 0.833 |
| nDCG@3 | 0.877 |
| Embed latency p50 | 0.021s |
| Embed latency p95 | 0.335s |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-smoke-20260524/results.jsonl`
- `/Volumes/PortableSSD/hermes-evals/embedding-benchmark/embedding-nomic-smoke-20260524/summary.md`

## Decision

`nomic-embed-text:latest` is fast and retrieves the target document within the top three for all seed cases, but it fails top-1 ranking for the recency/preference case.

This supports keeping it as the working rollback baseline while testing one of:

- recency-aware post-ranking
- `BAAI/bge-m3` in a separate `mem0_bge_m3_1024` collection
- `Qwen/Qwen3-Embedding-4B` if local runtime and memory use are acceptable
- a reranker such as `Qwen/Qwen3-Reranker-4B`

