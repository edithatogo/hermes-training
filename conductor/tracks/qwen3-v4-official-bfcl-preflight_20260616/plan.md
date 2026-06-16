# Plan: Qwen3 v4 Official BFCL Preflight

## Phase 1 - Preflight Harness

- [x] Task: add `scripts/check_official_bfcl_preflight.py`.
- [x] Task: check queue item identity, missing-suite status, run ID, BFCL CLI,
  SSD output root, and BFCL generate/evaluate command shape.
- [x] Task: probe an optional OpenAI-compatible endpoint through `/v1/models`.

## Phase 2 - Validation

- [x] Task: add `scripts/validate_official_bfcl_preflight.py`.
- [x] Task: add focused unit tests for blocked endpoint and ready-to-run states.
- [x] Task: wire the validator into `scripts/validate_readiness.py`.

## Phase 3 - Report And Boundary

- [x] Task: generate
  `reports/benchmark/official-candidates/qwen3-v4-official-bfcl-preflight-20260616.json`.
- [x] Task: generate
  `reports/benchmark/official-candidates/qwen3-v4-official-bfcl-preflight-20260616.md`.
- [x] Task: preserve the non-score boundary: the report is launch readiness
  only, not official BFCL evidence.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: BFCL CLI is executable on the SSD, the queue item is present and
  still fail-closed as missing, the exact run command is SSD-backed, and the
  current blocker is precisely recorded as no reachable/configured
  OpenAI-compatible endpoint.
- Remaining gap: official BFCL scoring still requires starting the Qwen3 v4
  adapter endpoint and running `bfcl generate` plus `bfcl evaluate`.
- Decision: complete this setup track. Do not mark `official-bfcl` coverage
  present until scored artifacts are ingested.
