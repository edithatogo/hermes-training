# Plan: Runtime Proof Queue Strict Endpoint Commands

## Phase 1 - Command Strictness

- [x] Task: Add strict scoring to endpoint command cards.
  - [x] Include `--require-no-extra-tool-text` for GGUF endpoint commands.
  - [x] Include `--require-no-extra-tool-text` for non-GGUF endpoint commands.
  - [x] Preserve endpoint artifact hints.

## Phase 2 - Regression Coverage

- [x] Task: Add focused unit checks.
  - [x] Verify GGUF endpoint commands are strict.
  - [x] Verify non-GGUF endpoint commands are strict.

## Phase 3 - Reports And Validation

- [x] Task: Regenerate `reports/benchmark/coverage/runtime-proof-action-queue-20260613.*`.
- [x] Task: Validate the runtime proof action queue.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: Runtime proof endpoint command cards now use strict no-extra-tool-text scoring by default.
- Validation: Focused runtime queue tests, runtime queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: No endpoint pilot was executed in this track.
- Decision: Complete. The queue now aligns endpoint proof commands with Hermes strict scoring.
