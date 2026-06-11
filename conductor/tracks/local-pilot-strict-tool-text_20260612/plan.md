# Plan: Local Pilot Strict Tool Text Gate

## Phase 1: Harness

- [x] Task: add `require_no_extra_tool_text` support to endpoint pilot scoring.
- [x] Task: expose `--require-no-extra-tool-text` in endpoint and local pilot
  runners.
- [x] Task: include strictness metadata in pilot summaries.
- [x] Task: add unit coverage for permissive versus strict tool-text scoring.

## Phase 2: Evidence

- [x] Task: rerun Gemma 4 E4B strict profile with no-extra-text scoring.
- [x] Task: document the difference between parsed-tool evidence and
  Hermes-strict evidence.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: strict local pilot claims can now require no leftover text while
  existing permissive pilot diagnostics remain available.
- Gaps: historical reports remain as originally scored and should be interpreted
  with their recorded command flags.
