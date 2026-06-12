# mem0 Run Card

Date: 2026-06-12T14:07:01.331669+00:00
Run ID: extraction-hermes4-14b-q4-smoke-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes4-14b-q4-smoke-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | extractor |
| Model/tool | `hermes-4-14b-q4` |
| Runtime | openai-compatible |
| Endpoint | `http://127.0.0.1:8092/v1` |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes4-14b-q4-smoke-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model hermes-4-14b-q4 \
  --base-url http://127.0.0.1:8092/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-hermes4-14b-q4-smoke-20260613
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.286 |
| Rerank pass rate |  |
| Recall@k / Recall@3 |  |
| Top-1 expected rate |  |
| Recency conflict pass rate |  |
| Distractor resistance pass rate |  |
| JSON validity rate | 0.286 |
| Add latency p50 |  |
| Search/embed/extract latency p50 | 0.355 |
| Search/embed/extract latency p95 | 2.204 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: reject for mem0 default

Reason: The extractor did not reach the JSON validity, durable extraction, and transient-noise gates needed for default promotion. It passed only 2/7 extraction cases, with JSON validity 0.286.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
