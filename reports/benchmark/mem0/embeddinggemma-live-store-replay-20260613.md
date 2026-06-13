# EmbeddingGemma Copied Live-Store Replay

Run ID: `embeddinggemma-live-store-replay-20260613`
Created: `2026-06-13T01:08:06.699308+00:00`

## Scope

This report compares a bounded, copied sample from the current default mem0 store against an
EmbeddingGemma candidate collection. Raw memory text is not committed; private raw artifacts
remain on the SSD path listed below.

## Metrics

| Metric | Value |
|---|---:|
| Queries | 5 |
| Unique copied memories | 4 |
| Comparable cases | 5 |
| Top-1 match rate | 0.200 |
| Default top recall@candidate-k | 1.000 |
| Mean overlap@candidate-k | 3.000 |

## Default Filter

| Field | Value |
|---|---|
| user_id | `default_user` |
| agent_id | `codex` |

## Redacted Case Results

| Query ID | Default count | Candidate count | Top-1 match | Recall | Default top hash | Candidate top hash |
|---|---:|---:|---|---|---|---|
| q01-hermes-current-recommended-strict-tool-c | 3 | 4 | no | yes | `17c6184b90ec` | `c1af96b939aa` |
| q02-mem0-default-rollback-embedder-and-colle | 3 | 4 | yes | yes | `c1af96b939aa` | `c1af96b939aa` |
| q03-embeddinggemma-candidate-collection-and- | 3 | 4 | no | yes | `17c6184b90ec` | `111db652b0cf` |
| q04-qwen3-v6-publication-gate-status | 3 | 4 | no | yes | `380609d0f870` | `17c6184b90ec` |
| q05-azure-or-colab-backend-priority-for-boun | 3 | 4 | no | yes | `380609d0f870` | `c1af96b939aa` |

## Artifacts

- Private raw export: `/Volumes/PortableSSD/hermes-evals/mem0-live-store-replay/embeddinggemma-live-store-replay-20260613/private-default-search-results.jsonl`
- Private raw candidate search: `/Volumes/PortableSSD/hermes-evals/mem0-live-store-replay/embeddinggemma-live-store-replay-20260613/private-candidate-search-results.jsonl`
- Redacted summary JSON: `/Volumes/PortableSSD/hermes-evals/mem0-live-store-replay/embeddinggemma-live-store-replay-20260613/summary-redacted.json`
- Candidate config: `/Volumes/PortableSSD/hermes-evals/mem0-live-store-replay/embeddinggemma-live-store-replay-20260613/candidate-config.json`
- Candidate collection: `mem0_embeddinggemma_300m_768_embeddinggemma-live-store-replay-20260613`

## Decision

EmbeddingGemma did not fully match the current default on the copied-live-store replay; keep it opt-in.

## Rollback

No live default config was edited. Rollback remains `unset MEM0_CONFIG_PATH` and the
current `nomic-embed-text:latest` / `mem0_nomic_768` default path.
