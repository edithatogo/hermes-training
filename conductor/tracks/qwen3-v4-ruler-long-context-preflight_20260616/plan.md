# Plan: Qwen3 v4 RULER Long-Context Preflight

## Phase 1 - Queue Command

- [x] Task: replace `<context>` with the first-stage 4096-token RULER command.
- [x] Task: update queue validation so placeholder contexts fail.

## Phase 2 - Preflight Harness

- [x] Task: add `scripts/check_ruler_long_context_preflight.py`.
- [x] Task: record the context ladder and RULER module availability.
- [x] Task: add `scripts/validate_ruler_long_context_preflight.py`.
- [x] Task: add focused unit tests for blocked and ready states.

## Phase 3 - Report And Readiness

- [x] Task: generate
  `reports/benchmark/official-candidates/qwen3-v4-ruler-long-context-preflight-20260616.json`.
- [x] Task: generate
  `reports/benchmark/official-candidates/qwen3-v4-ruler-long-context-preflight-20260616.md`.
- [x] Task: wire the validator into `scripts/validate_readiness.py`.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: the queue now has a concrete ctx4096 first-stage command, the
  preflight records the 4096/8192/16384 context ladder, and the current blocker
  is precisely identified as no `ruler` module in the SSD benchmark environment.
- Remaining gap: RULER is not installed/proven, and no RULER scores exist.
- Decision: complete this setup track. Do not mark `ruler-long-context`
  coverage present until scored RULER artifacts are ingested.
