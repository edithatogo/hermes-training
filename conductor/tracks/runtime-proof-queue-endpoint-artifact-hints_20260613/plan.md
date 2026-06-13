# Plan: Runtime Proof Queue Endpoint Artifact Hints

## Phase 1 - Command Text

- [x] Task: Make endpoint artifact hints conditional.
  - [x] Keep GGUF-specific text for GGUF candidates.
  - [x] Use runtime-neutral local artifact text for non-GGUF endpoint candidates.

## Phase 2 - Regression Coverage

- [x] Task: Add a non-GGUF endpoint candidate test.
  - [x] Verify the endpoint pilot harness is still used.
  - [x] Verify the command mentions a compatible local artifact.
  - [x] Verify the command does not mention a GGUF-only artifact.

## Phase 3 - Reports And Validation

- [x] Task: Regenerate `reports/benchmark/coverage/runtime-proof-action-queue-20260613.*`.
- [x] Task: Validate the runtime proof action queue.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: `openbmb/MiniCPM-V-4.6-GPTQ` now renders a runtime-neutral endpoint pilot command card.
- Validation: Focused runtime queue tests, runtime queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: No endpoint pilot was executed in this track.
- Decision: Complete. Queue guidance is more accurate without making new runtime claims.
