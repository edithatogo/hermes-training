# Plan: mem0 Queue Differentiation Suite Commands

## Phase 1 - Suite Selection

- [x] Task: Add an embedding suite selector.
  - [x] Use the differentiation suite for `first_gate: differentiation-suite`.
  - [x] Use the differentiation suite for benchmarked/source-benchmarked embedding candidates.
  - [x] Keep baseline smoke candidates on the smaller retrieval suite.

## Phase 2 - Regression Coverage

- [x] Task: Add focused command tests.
  - [x] Verify BGE-M3 uses the differentiation suite.
  - [x] Verify Jina v5 omni text-matching MLX uses the differentiation suite when its gate requires it.

## Phase 3 - Reports And Validation

- [x] Task: Regenerate `reports/model-radar/mem0-candidate-queue.md`.
- [x] Task: Validate the mem0 candidate queue.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: Generated mem0 command cards now match documented differentiation-suite gates for benchmarked embedding candidates.
- Validation: Focused mem0 queue tests, mem0 queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: No benchmark rerun was performed in this track.
- Decision: Complete. The queue is more faithful to the benchmark plan without changing defaults.
