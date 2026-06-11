# Plan: Local Pilot Score Wrapper

## Phase 1: Harness Support

- [x] Task: add score-prefix and score-suffix arguments to the local pilot
  runner.
- [x] Task: preserve raw responses while scoring wrapped responses.
- [x] Task: add unit coverage for wrapper construction.

## Phase 2: Prompt-Repair Retry

- [x] Task: run Qwen3.5 0.8B through the BFCL-style pilot with a tool-call
  prefill and scoring wrapper.
- [x] Task: document the failure mode.

## Phase 3: Validation

- [x] Task: run unit, queue, candidate, readiness, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: the harness preserves raw output and records scored wrappers; the
  Qwen3.5 0.8B wrapper retry is documented fail-closed.
- Gaps: no prompt-repair profile passed; strict tool-call promotion remains
  blocked.
