# Specification: Tiny Helper Standard Benchmark Execution

## Overview

The tiny helper lane is now defined and its prompt coverage is validated. This
track executes the lightweight standard benchmark subsets that the repo uses to
decide whether a lane can move beyond runtime/helper evidence.

Primary candidates:

- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`
- `openbmb/MiniCPM5-1B-MLX`

Comparison lane:

- `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF`

## Goals

- Run the lane-appropriate standard benchmark subsets for the tiny helper
  candidates.
- Capture the exact commands, outputs, and decision status.
- Keep the results separate from the stricter publication gate.
- Record whether any candidate is still runtime-only, helper-ready, or blocked.

## Functional Requirements

1. Use the existing prompt coverage and helper profile as the baseline.
2. Execute the Hermes-local expanded prompt set and the supported subset
   benchmarks that apply to the lane.
3. Record outputs under SSD-backed benchmark artifact directories.
4. Capture the pass/fail status for each candidate and each benchmark subset.
5. Update the benchmark reports and handoff notes with the outcome.

## Non-Functional Requirements

- Keep all artifacts on SSD-backed storage.
- Prefer lightweight local subsets before any broader suite.
- Do not claim publication readiness from subset results alone.
- Keep the execution repeatable from documented commands.

## Acceptance Criteria

- The standard benchmark subsets have been executed or explicitly blocked.
- The run cards and result summaries are written to `reports/benchmark/`.
- The helper lane decision is explicit in the docs.
- Validation passes.

## Out of Scope

- Full BFCL or full lm-eval publication claims.
- Hugging Face adapter publication.
- Large teacher-model benchmarking.
- New model discovery.
