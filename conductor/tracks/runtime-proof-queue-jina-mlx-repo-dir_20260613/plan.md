# Plan: Runtime Proof Queue Jina MLX Repo Dir

## Phase 1 - Command Template

- [x] Task: Remove the literal Jina MLX repo-dir placeholder.
  - [x] Rely on the runner's default SSD-backed repo directory.
  - [x] Keep `--local-files-only` in generated proof commands.
  - [x] Add acquisition guidance to the command comment.

## Phase 2 - Regression Coverage

- [x] Task: Add Jina MLX command tests.
  - [x] Verify text-matching candidates use `--task-type text-matching`.
  - [x] Verify retrieval candidates use `--task-type retrieval`.
  - [x] Verify generated commands contain no `<repo-dir>` placeholder.

## Phase 3 - Reports And Validation

- [x] Task: Regenerate `reports/benchmark/coverage/runtime-proof-action-queue-20260613.*`.
- [x] Task: Validate the runtime proof action queue.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: Jina MLX support-model queue commands now rely on the benchmark runner's SSD default and remain fail-closed for unacquired artifacts.
- Validation: Focused runtime queue tests, runtime queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: No Jina benchmark was rerun in this track.
- Decision: Complete. Queue guidance is executable without making new performance claims.
