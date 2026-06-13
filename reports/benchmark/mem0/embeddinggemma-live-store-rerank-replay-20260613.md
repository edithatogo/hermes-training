# EmbeddingGemma Live-Store Rerank Replay

Run ID: `embeddinggemma-live-store-rerank-replay-20260613`
Created: `2026-06-13T01:16:19.249138+00:00`

## Scope

This report replays local reranking strategies over the private copied
live-store replay artifacts. Raw memory text is not committed; committed
case rows use hashes only.

## Strategy Metrics

| Strategy | Comparable cases | Top-1 match | Default-top recall | Mean default-top rank | Decision |
|---|---:|---:|---:|---:|---|
| `vector` | 5 | 0.200 | 1.000 | 2.600 | does not pass |
| `query_terms_guarded` | 5 | 0.200 | 1.000 | 2.600 | does not pass |
| `score_plus_created_at_rank` | 5 | 0.200 | 1.000 | 2.600 | does not pass |
| `score_plus_created_at_rank_close_margin` | 5 | 0.200 | 1.000 | 2.600 | does not pass |

## Best Strategy Cases

Best strategy: `vector`

| Query ID | Default count | Candidate count | Top-1 match | Recall | Default top rank | Default top hash | Candidate top hash |
|---|---:|---:|---|---|---:|---|---|
| q01-hermes-current-recommended-strict-tool-c | 3 | 4 | no | yes | 3 | `17c6184b90ec` | `c1af96b939aa` |
| q02-mem0-default-rollback-embedder-and-colle | 3 | 4 | yes | yes | 1 | `c1af96b939aa` | `c1af96b939aa` |
| q03-embeddinggemma-candidate-collection-and- | 3 | 4 | no | yes | 3 | `17c6184b90ec` | `111db652b0cf` |
| q04-qwen3-v6-publication-gate-status | 3 | 4 | no | yes | 2 | `380609d0f870` | `17c6184b90ec` |
| q05-azure-or-colab-backend-priority-for-boun | 3 | 4 | no | yes | 4 | `380609d0f870` | `c1af96b939aa` |

## Artifacts

- Private default replay JSONL: `/Volumes/PortableSSD/hermes-evals/mem0-live-store-replay/embeddinggemma-live-store-replay-20260613/private-default-search-results.jsonl`
- Private candidate replay JSONL: `/Volumes/PortableSSD/hermes-evals/mem0-live-store-replay/embeddinggemma-live-store-replay-20260613/private-candidate-search-results.jsonl`
- Private redacted summary JSON: `/Volumes/PortableSSD/hermes-evals/mem0-live-store-rerank-replay/embeddinggemma-live-store-rerank-replay-20260613/summary-redacted.json`

## Decision

No existing rerank strategy fully restores default top-1 order; keep EmbeddingGemma opt-in and non-default.
