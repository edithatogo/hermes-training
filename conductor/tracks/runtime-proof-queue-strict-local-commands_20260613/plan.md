# Plan: Runtime Proof Queue Strict Local Commands

## Phase 1 - Command Strictness

- [x] Task: Add strict scoring to local queue command cards.
  - [x] Add `--require-no-extra-tool-text` for MLX runtime proof commands.
  - [x] Add `--require-no-extra-tool-text` for prompt-profile repair commands.

## Phase 2 - Regression Coverage

- [x] Task: Add focused unit checks.
  - [x] Verify MLX runtime proof commands are strict.
  - [x] Verify prompt-profile repair commands are strict.

## Phase 3 - Reports And Validation

- [x] Task: Regenerate `reports/benchmark/coverage/runtime-proof-action-queue-20260613.*`.
- [x] Task: Validate the runtime proof action queue.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: Local MLX and prompt-profile queue command cards now use strict no-extra-tool-text scoring.
- Validation: Focused runtime queue tests, runtime queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: No local pilot was executed in this track.
- Decision: Complete. Local queue commands now align with Hermes strict scoring.
