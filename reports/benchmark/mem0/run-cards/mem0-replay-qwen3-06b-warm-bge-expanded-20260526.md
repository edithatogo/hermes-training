# mem0 Run Card

Date: 2026-05-25T17:09:30.631594+00:00
Run ID: mem0-replay-qwen3-06b-warm-bge-expanded-20260526
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/mem0-replay-qwen3-06b-warm-bge-expanded-20260526/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | `Qwen/Qwen3-Reranker-0.6B` |
| Runtime | qwen3_causal_lm |
| Endpoint | |
| Collection or index | |
| Embedding dims |  |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-reranking-replay/mem0-replay-qwen3-06b-warm-bge-expanded-20260526` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_rerank_replay.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-0.6B \
  --qwen3-device auto \
  --qwen3-max-length 4096 \
  --qwen3-local-files-only \
  --qwen3-server-url http://127.0.0.1:8765 \
  --suite /Volumes/PortableSSD/hermes-evals/mem0-reranking-benchmark/bge-m3-expanded-derived-reranking-20260526/candidate-suite.json \
  --run-id mem0-replay-qwen3-06b-warm-bge-expanded-20260526
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 1.000 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 1.000 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 1.000 |
| JSON validity rate |  |
| Add latency p50 |  |
| Search/embed/extract latency p50 |  |
| Search/embed/extract latency p95 |  |
| Rerank latency p50 | 0.281 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The replay suite passed through the read-only wrapper path; keep it as integration evidence and require live multi-result or isolated-store proof before default promotion.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
