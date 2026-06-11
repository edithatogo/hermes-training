# Plan: BitNet Native Runtime Smoke

## Phase 1: Preflight Accuracy

- [x] Task: update the specialist preflight to detect absolute executable
  runtime paths.
- [x] Task: regenerate the specialist-runtime preflight report.

## Phase 2: Native Runtime Smoke

- [x] Task: run the local BitNet wrapper from the BitNet checkout with a tiny
  deterministic prompt.
- [x] Task: capture load, generation, timing, and memory evidence.

## Phase 3: Documentation And Validation

- [x] Task: record the runtime report and update queue/candidate/handoff notes.
- [x] Task: run schema checks, unit tests, readiness validation, and whitespace
  checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: native BitNet load and 16-token generation completed from SSD-backed
  artifacts with exit code 0.
- Gaps: output was not instruction-compliant JSON, so this is a runtime proof
  only and not a Hermes readiness claim.
