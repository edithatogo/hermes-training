# Plan: Prompt/Profile Repair Queue

## Phase 1 - Queue Builder

- [x] Task: Build prompt/profile repair rows from the all-candidate coverage report.
  - [x] Filter only Hermes strict-format and empty strict-prompt blockers.
  - [x] Attach family-specific repair hypotheses.
  - [x] Emit no-download local or endpoint rerun commands.

## Phase 2 - Deterministic Validation

- [x] Task: Add a validator for generated reports.
  - [x] Require the JSON and Markdown reports to exist.
  - [x] Require repair hypotheses and strict no-extra-tool-text scoring.
  - [x] Regenerate with the recorded timestamp and fail if reports are stale.

## Phase 3 - Readiness And Documentation

- [x] Task: Add unit tests and full readiness wiring.
- [x] Task: Generate the prompt/profile repair queue reports.
- [x] Task: Update the Conductor registry and handoff.

## Phase 4 - Route Correction

- [x] Task: Route candidates with GGUF/endpoint evidence to endpoint repair commands even when their nominal environment is `mac-mlx`.
- [x] Task: Add a regression test for the EXAONE GGUF-proven / MLX-blocked case.
- [x] Task: Regenerate the prompt/profile repair queue.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: Queue generation is deterministic, no-download, readiness-gated,
  and scoped to candidates whose next useful work is prompt/profile repair.
  EXAONE 1.2B is routed through the GGUF endpoint path instead of blocked MLX
  loading.
- Validation: Focused unit tests, queue validator, Conductor consistency, and
  full hub readiness are required before commit.
- Gaps: This track does not execute the queued repairs.
- Decision: Complete. The queue is ready for subsequent one-by-one local repair
  runs.
