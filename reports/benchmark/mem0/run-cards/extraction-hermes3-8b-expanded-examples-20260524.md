# mem0 Run Card

Date: 2026-05-24T07:56:56.656558+00:00
Run ID: extraction-hermes3-8b-expanded-examples-20260524
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes3-8b-expanded-examples-20260524/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | extractor |
| Model/tool | `hermes3:8b` |
| Runtime | openai-compatible |
| Endpoint | `http://127.0.0.1:11434/v1` |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes3-8b-expanded-examples-20260524` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model hermes3:8b \
  --base-url http://127.0.0.1:11434/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-hermes3-8b-expanded-examples-20260524
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.571 |
| Rerank pass rate |  |
| Recall@k / Recall@3 |  |
| Top-1 expected rate |  |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate | 0.714 |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 1.476 |
| Search/embed/extract latency p95 | 2.423 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The extractor did not reach the JSON validity, durable extraction, and transient-noise gates needed for default promotion.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
