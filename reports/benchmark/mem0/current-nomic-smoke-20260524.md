# mem0 Current Nomic Smoke

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool cmd \
  --suite benchmarks/mem0_memory/smoke_suite.json \
  --run-id mem0-current-nomic-smoke-20260524
```

## Runtime

| Component | Value |
|---|---|
| mem0 vector store | Qdrant |
| Collection | `mem0_nomic_768` |
| Embedder | `nomic-embed-text:latest` through Ollama |
| Extraction / LLM | `sam860/LFM2:2.6b` through Ollama |
| Tool namespace | `cmd` |

## Result

| Metric | Score |
|---|---:|
| Cases | 3 |
| Pass rate | 0.667 |
| Recall@k | 1.000 |
| Top-1 expected rate | 0.667 |
| Recency conflict pass rate | 0.000 |
| Distractor resistance pass rate | 1.000 |
| Add latency p50 | 3.376s |
| Search latency p50 | 3.388s |
| Search latency p95 | 3.399s |
| Cleanup successes | 6 / 6 |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524/results.jsonl`
- `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-smoke-20260524/summary.md`

## Decision

The current mem0 stack is functional but not good enough to treat as a quality baseline for recency-sensitive memory.

The direct recall and distractor cases passed. The recency-conflict case failed because the older conflicting preference ranked above the newer current preference. This is the first concrete reason to test either:

- recency-aware ranking on top of current Qdrant results
- a reranker such as Qwen3-Reranker-4B
- a stronger embedding model in a separate collection
- extraction metadata that marks superseded memories

Keep `nomic-embed-text:latest` as the rollback default until a candidate beats this result and preserves current add/search reliability.

