# mem0 Run Card

Date:
Run ID:

## Candidate

| Field | Value |
|---|---|
| Role | extractor / embedder / reranker / retriever / store |
| Model | |
| Runtime | Ollama / llama.cpp / LM Studio / MLX / Transformers / other |
| Endpoint | |
| Collection or index | |
| Embedding dims | |
| Distance metric | |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --suite benchmarks/mem0_memory/smoke_suite.json \
  --run-id <run-id>
```

## Result

| Metric | Value |
|---|---:|
| Pass rate | |
| Recall@k | |
| Top-1 expected rate | |
| Recency conflict pass rate | |
| Distractor resistance pass rate | |
| Add latency p50 | |
| Search latency p50 | |
| Search latency p95 | |

## Decision

Promote / keep testing / reject:

Reason:

Rollback:

