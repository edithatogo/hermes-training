# Spec: mem0 Guarded Read Wrapper

## Goal

Provide a stable read-only entrypoint for local Hermes agents that applies the
validated close-margin mem0 reranker without changing mem0 defaults.

## Requirements

- Default to `score_plus_created_at_rank_close_margin`.
- Expose explicit `vector` and `qwen3` modes for comparison and future gates.
- Preserve read-only behavior and report that the wrapper does not mutate mem0
  config.
- Allow optional Qwen fallback to vector ordering when the local service is not
  available.
- Emit structured JSON with selected strategy, latency, input count, and ranked
  results.
- Document usage, rollback, and promotion boundaries.

## Non-Goals

- Do not modify `~/.mem0/config.json`.
- Do not change the default `mem0_nomic_768` collection.
- Do not promote Qwen3 as the default until a recency-aware fixture passes.
