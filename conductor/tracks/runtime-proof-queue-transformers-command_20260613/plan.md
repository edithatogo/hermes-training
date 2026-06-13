# Plan: Runtime Proof Queue Transformers Command

## Phase 1 - Command Template

- [x] Task: Add a concrete `hf-transformers` runtime proof command.
  - [x] Point at `scripts/run_transformers_pilot_benchmark.py`.
  - [x] Use the BFCL pilot suite.
  - [x] Include strict no-extra-tool-text scoring.
  - [x] Surface the SSD-backed Hugging Face cache guardrail.

## Phase 2 - Tests And Reports

- [x] Task: Add focused unit coverage.
  - [x] Verify the command uses the bounded Transformers pilot.
  - [x] Verify strict and device flags are present.
- [x] Task: Regenerate runtime proof action queue artifacts.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: `reports/benchmark/coverage/runtime-proof-action-queue-20260613.md` now emits an executable bounded Transformers pilot command for `hf-transformers` queue entries.
- Validation: Focused queue tests, runtime proof queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: The command has not been executed against the candidate in this track.
- Decision: Complete. The track improves next-action quality without making benchmark claims.
