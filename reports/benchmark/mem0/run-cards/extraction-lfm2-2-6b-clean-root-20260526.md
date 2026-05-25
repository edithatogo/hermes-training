# mem0 Run Card

Date: 2026-05-25T16:15:36.852166+00:00
Run ID: extraction-lfm2-2-6b-clean-root-20260526
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-clean-root-20260526/summary.json`

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
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-clean-root-20260526` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model sam860/LFM2:2.6b \
  --base-url http://127.0.0.1:11434/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-lfm2-2-6b-clean-root-20260526
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
| Search/embed/extract latency p50 | 0.874 |
| Search/embed/extract latency p95 | 0.988 |
| Rerank latency p50 |  |

## Decision

Promote / keep testing / reject: keep testing

Reason: The extractor passed the strict JSON, durable extraction, forbidden-hit, and empty-case gates; keep it as the rollback extractor until a larger replacement suite or stronger model beats it.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
