# Implementation Plan

## Phase 1: Replay Harness

- [x] Task: Add offline rerank replay script
    - [x] Read private default and candidate JSONL artifacts.
    - [x] Group cases by query id.
    - [x] Evaluate existing local rerank strategies.
    - [x] Render only redacted hash-level reports.
- [x] Task: Add focused tests
    - [x] Validate default-top recall and rank accounting.
    - [x] Validate committed report text excludes raw memory text.

## Phase 2: Evidence And Docs

- [x] Task: Run replay against copied live-store artifacts
    - [x] Record strategy-level metrics.
    - [x] Commit redacted report under `reports/benchmark/mem0/`.
- [x] Task: Update docs
    - [x] Update mem0 candidate and benchmark notes.
    - [x] Update report index and track registry.
- [x] Task: Validate and publish
    - [x] Run focused tests.
    - [x] Run mem0 evidence/model-candidate checks.
    - [x] Run structural readiness.
    - [x] Commit and push.

## Health Target

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: offline replay over the copied live-store artifacts tested
  `vector`, `query_terms_guarded`, `score_plus_created_at_rank`, and
  `score_plus_created_at_rank_close_margin`; all stayed at top-1 `0.200` with
  default-top recall `1.000`, so the default-promotion blocker is now explicit.
- Remaining gaps: a future track can test a learned reranker or explicit
  migration policy if accepting changed ordering becomes desirable.
