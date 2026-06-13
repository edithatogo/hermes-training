# Implementation Plan

## Phase 1: Guarded Replay Strategy

- [x] Task: Add query-aware guarded reranker
    - [x] Add query tokenization and negated-runtime/path penalties.
    - [x] Expose `query_terms_guarded` in rerank search and fixed-suite paths.
    - [x] Include the query when passing candidates to the guarded reranker.
- [x] Task: Add captured fixture replay support
    - [x] Load candidates from live fixture `results.jsonl`.
    - [x] Infer expected fragments from the source live fixture suite.
    - [x] Record replay source suite and source strategy in summaries.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Evidence And Documentation

- [x] Task: Run replay comparison
    - [x] Re-run vector replay over captured EmbeddingGemma live fixture
      candidates.
    - [x] Re-run `query_terms_guarded` replay over the same candidates.
    - [x] Generate run cards for both replay runs.
- [x] Task: Update mem0 benchmark and radar documentation
    - [x] Update mem0 differentiation summary and run-card index.
    - [x] Update `MODEL_CANDIDATES.yaml`.
    - [x] Update `FUTURE_MODELS.md`.
- [x] Task: Validate
    - [x] Run focused mem0 rerank/run-card unit tests.
    - [x] Run mem0 evidence validation.
    - [x] Run mem0 model-candidate validation.
    - [x] Run hub readiness validation.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Health Target

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: replay comparison reproduced vector top-1 `0.909` and guarded
  top-1 `1.000`; the follow-on resilient-proxy live fixture passed at top-1
  `1.000` / recall@3 `1.000`; focused tests pass, mem0 evidence validation
  passes, model candidate validation passes, and hub readiness passes.
- Remaining gaps: EmbeddingGemma remains non-default until resilient proxy
  integration, rollback behavior, and the default collection migration decision
  are documented.
