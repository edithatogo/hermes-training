# Plan: mem0 Queue Blocked Command Guard

## Phase 1 - Command Guard

- [x] Task: Add fail-closed command cards.
  - [x] Guard `access-gated` candidates.
  - [x] Guard `runtime-blocked` candidates.
  - [x] Keep candidate IDs and unblock instructions visible.

## Phase 2 - Regression Coverage

- [x] Task: Add focused tests.
  - [x] Verify access-gated candidates do not emit sentence-transformers benchmark commands.
  - [x] Verify runtime-blocked candidates do not emit sentence-transformers benchmark commands.

## Phase 3 - Reports And Validation

- [x] Task: Regenerate `reports/model-radar/mem0-candidate-queue.md`.
- [x] Task: Validate the mem0 candidate queue.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: Blocked mem0 candidates now render unblock notes instead of known-failing benchmark commands.
- Validation: Focused mem0 queue tests, mem0 queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: None for the local command-generation fix.
- Decision: Complete. The queue now fails closed for blocked candidates.
