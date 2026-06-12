# mem0 Run Card

Date: 2026-06-12T14:16:58.973608+00:00
Run ID: mem0-fixture-jina-v5-text-matching-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-fixture-jina-v5-text-matching-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | reranker |
| Model/tool | `cmd` |
| Runtime | score_plus_created_at_rank_close_margin |
| Endpoint | |
| Collection or index | `mem0_fixture_mem0_fixture_jina_v5_text_matching_20260613` |
| Embedding dims | 1024 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-fixture-jina-v5-text-matching-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --run-id mem0-fixture-jina-v5-text-matching-20260613 \
  --embedder-provider openai \
  --embedder-model jinaai/jina-embeddings-v5-omni-small-text-matching-mlx \
  --embedder-base-url http://127.0.0.1:8094/v1 \
  --embedding-dims 1024 \
  --skip-qwen3 \
  --timeout-s 120
```

## Result

| Metric | Value |
|---|---:|
| Pass rate / top-1 accuracy | 0.800 |
| Rerank pass rate |  |
| Recall@k / Recall@3 | 1.000 |
| Top-1 expected rate | 0.800 |
| Recency conflict pass rate | 1.000 |
| Distractor resistance pass rate | 1.000 |
| JSON validity rate |  |
| Add latency p50 | 3.039 |
| Search/embed/extract latency p50 | 2.978 |
| Search/embed/extract latency p95 | 3.030 |
| Rerank latency p50 | 0.000 |

## Strategy Comparison

| Strategy | Pass | Top-1 | Recall@3 | MRR | nDCG@3 | p50 rerank |
|---|---:|---:|---:|---:|---:|---:|
| `vector` | 0.600 | 0.600 | 1.000 | 0.800 | 0.852 | 0.000 |
| `score_plus_created_at_rank_close_margin` | 0.800 | 0.800 | 1.000 | 0.900 | 0.926 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The isolated fixture proved the 1024-dim Jina endpoint/config path, but it did not prove strict multi-result top-1 behavior. The close-margin strategy still missed the tool-state current-collection case, so this remains a comparison baseline.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
