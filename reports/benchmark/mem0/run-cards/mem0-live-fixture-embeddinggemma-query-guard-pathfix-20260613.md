# mem0 Run Card

Date: 2026-06-13T00:47:30.070906+00:00
Run ID: mem0-live-fixture-embeddinggemma-query-guard-pathfix-20260613
Summary: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-embeddinggemma-query-guard-pathfix-20260613/summary.json`

## Candidate

| Field | Value |
|---|---|
| Role | memory+embedder fixture |
| Model/tool | `cmd` |
| Runtime | openai embedder + vector |
| Endpoint | `http://127.0.0.1:8105/v1` |
| Collection or index | `mem0_fixture_mem0_live_fixture_embeddinggemma_query_guard_pathfix_20260613` |
| Embedding dims | 768 |
| Distance metric | cosine / configured vector-store metric |
| Output | `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-live-fixture-embeddinggemma-query-guard-pathfix-20260613` |

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --keep-fixture \
  --embedder-provider openai \
  --embedder-model embeddinggemma-300m-qat-Q4_0.gguf \
  --embedder-base-url http://127.0.0.1:8105/v1 \
  --embedding-dims 768 \
  --skip-qwen3 \
  --suite benchmarks/mem0_memory/live_fixture_differentiation_suite.json \
  --run-id mem0-live-fixture-embeddinggemma-query-guard-pathfix-20260613
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
| Add latency p50 | 2.945 |
| Search/embed/extract latency p50 | 2.946 |
| Search/embed/extract latency p95 | 3.457 |
| Rerank latency p50 | 0.000 |

## Strategy Comparison

| Strategy | Pass | Top-1 | Recall@3 | MRR | nDCG@3 | p50 rerank |
|---|---:|---:|---:|---:|---:|---:|
| `vector` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| `score_plus_created_at_rank_close_margin` | 0.909 | 0.909 | 1.000 | 0.939 | 0.955 | 0.000 |
| `query_terms_guarded` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |

## Decision

Promote / keep testing / reject: keep testing

Reason: The isolated fixture passed the live add/search multi-result gate without touching defaults; require a deliberate default-integration plan before promotion.

Rollback: Keep `nomic-embed-text:latest`, `mem0_nomic_768`, and `sam860/LFM2:2.6b` available unless this card documents a safer replacement.
