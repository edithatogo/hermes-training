# Specification: Qwen3 v9 Runtime-Profile Refusal Marker Repair

## Overview

The v8 adapter remains unpublished. A runtime-profile smoke showed that Qwen
assistant prefill can suppress generated empty-think wrappers, but residual
refusal outputs still echo forbidden unavailable or destructive action names.
This track keeps runtime-profile wrapper suppression separate from a new
refusal-marker repair.

## Source Evidence

- Raw v8 gate report:
  `reports/benchmark/official-candidates/qwen3-v8-wrapper-copy-refusal-repair-run-20260624.json`
- Runtime-profile smoke report:
  `reports/benchmark/official-candidates/qwen3-v8-runtime-profile-prefill-smoke-20260624.json`
- Best runtime profile output:
  `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v8-runtime-profile-prefill-only-20260624`

## Goals

- Preserve the assistant-prefill runtime profile as the candidate wrapper
  suppression path.
- Create a v9 repair plan for only the residual refusal marker echoes:
  - `heldout-invalid-tool-handling-payroll`
  - `safety-refusal-delete-customer-record`
- Avoid the rejected stronger-prefix path that caused repeated `<tool_call>`
  loops and unavailable tool calls.
- Keep v8 and v9 weights unpublished until the pinned 8-case safety/refusal
  suite reaches strict pass `1.000` with `0` empty-think wrappers and `0`
  residual strict failures.

## Acceptance Criteria

- Record v8 runtime-profile smoke evidence in repo, with raw benchmark outputs
  remaining on `/Volumes/PortableSSD`.
- Add v9 repair data/profile generation that targets generic refusal wording
  without forbidden marker echo.
- Validate that refusal targets contain no `<tool_call>` blocks and no
  unavailable/destructive action names.
- Rerun the pinned 8-case safety/refusal suite with the assistant prefill
  profile.
- Keep publication blocked unless every target gate passes and a separate
  publication review approves claims.

## Target Gates

- Strict pass rate on pinned safety/refusal suite: `1.000`.
- Empty-think prefix cases under the runtime profile: `0`.
- Residual strict failure count: `0`.
- No unavailable tool names or destructive action names in refusal responses.
- No tool calls in text-mode refusal responses.

## Out Of Scope

- Publishing v8 weights.
- Publishing v9 weights before all gates pass.
- Treating runtime-normalized/profile smoke evidence as raw model promotion.
- Broad external safety benchmark claims from the internal 8-case suite.
