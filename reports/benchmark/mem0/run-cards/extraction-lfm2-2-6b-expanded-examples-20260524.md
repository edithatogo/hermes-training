# mem0 Run Card

Date: 2026-05-24T07:56:56.553605+00:00
Run ID: extraction-lfm2-2-6b-expanded-examples-20260524
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-expanded-examples-20260524/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | extractor |
| Model/tool | `sam860/LFM2:2.6b` |
| Runtime | openai-compatible |
| Endpoint | `http://127.0.0.1:11434/v1` |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-expanded-examples-20260524` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model sam860/LFM2:2.6b \
  --base-url http://127.0.0.1:11434/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-lfm2-2-6b-expanded-examples-20260524
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 1.000 |
| Rerank pass rate |  |
| Recall@k / Recall@3 |  |
| Top-1 expected rate |  |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate | 1.000 |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 1.847 |
| Search/embed/extract latency p95 | 2.128 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The extractor did not reach the JSON validity, durable extraction, and transient-noise gates needed for default promotion.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
