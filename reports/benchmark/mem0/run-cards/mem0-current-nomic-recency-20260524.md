# mem0 Run Card

Date: 2026-05-24T06:54:29.885526+00:00
Run ID: mem0-current-nomic-recency-20260524
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-20260524/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | memory |
| Model/tool | `cmd` |
| Runtime | cmd |
| Endpoint | |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-memory-benchmark/mem0-current-nomic-recency-20260524` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py \
  --tool cmd \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --run-id mem0-current-nomic-recency-20260524
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.400 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.400 |
| Recency conflict pass rate | 0.000 |
| Distractor resistance pass rate | 1.000 |
| JSON validity rate |  |
| Add latency p50 | 2.905 |
| Search/embed/extract latency p50 | 2.890 |
| Search/embed/extract latency p95 | 3.798 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The current mem0 path is functional and rollback-safe, but this run did not reach the strict 1.000 pass gate.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
