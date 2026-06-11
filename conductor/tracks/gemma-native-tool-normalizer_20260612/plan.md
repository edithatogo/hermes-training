# Plan: Gemma Native Tool Normalizer Analysis

## Phase 1: Harness Support

- [x] Task: add Gemma native `function` payload conversion as an opt-in
  score-only normalizer.
- [x] Task: expose the normalizer in `scripts/run_local_pilot_benchmark.py`.
- [x] Task: include score-normalizer metadata in pilot summaries.
- [x] Task: add unit tests for conversion and refusal-preservation behavior.

## Phase 2: Evidence

- [x] Task: run Gemma 4 E4B through the BFCL-style pilot with
  `--score-normalizer gemma-native-tool-call`.
- [x] Task: document rescued and still-failing cases.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: the normalizer is opt-in, tested, raw-preserving, and records only
  runtime-adapter evidence. The normalized Gemma pilot improved from 0/3 to 1/3
  but remains fail-closed.
- Gaps: no endpoint adapter exists yet; strict raw Gemma remains blocked.
