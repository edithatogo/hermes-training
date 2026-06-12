# Plan: Qwen Retrieval Tiny Refresh

## Phase 1: Source Verification

- [x] Task: verify the official Qwen3-Embedding-0.6B and Qwen3-Reranker-0.6B pages.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the verified 0.6B retrieval pair.
- [x] Task: update `FUTURE_MODELS.md` with the small retrieval shortlist entries.
- [x] Task: update `HANDOFF.md` with the new guidance.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the lane is small, official, and already benchmark-adjacent.
- Gaps: none beyond optional embedding runtime proof.
