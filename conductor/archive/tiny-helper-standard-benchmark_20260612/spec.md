# Specification: Tiny Helper Standard Benchmark Matrix

## Overview

The tiny helper lane now exists as an explicit runtime contract. This track
turns that lane into a benchmarkable, publication-aware work item by recording
the standard benchmark matrix that applies to the smallest helper candidates and
their current readiness state.

The candidates in scope are:

- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`
- `openbmb/MiniCPM5-1B-MLX`
- `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF` as a comparison lane only

## Goals

- Record which standardized benchmarks are relevant for the tiny helper lane.
- Separate Hermes-local evidence from broader standardized benchmark evidence.
- Mark what is already proven, what is blocked, and what remains to run.
- Keep publication claims constrained to the exact evidence available.

## Functional Requirements

1. Define the benchmark matrix for the tiny helper lane using
   `STANDARD_BENCHMARKS.md`.
2. Record the current evidence status for Hermes-local, BFCL-style, coding,
   lm-eval, and safety coverage.
3. Clarify that the tiny helper lane is not a publication candidate until the
   required standardized evidence exists.
4. Update the maintained docs and track notes so the benchmark status is easy
   to find.
5. Keep the work limited to documentation and evidence mapping unless a
   lightweight local benchmark is already available.

## Non-Functional Requirements

- Prefer existing local evidence over speculative benchmark claims.
- Keep SSD-backed artifact locations explicit.
- Avoid over-promoting helper lanes into chat or publication candidates.
- Preserve the repo's existing benchmark contract language.

## Acceptance Criteria

- The standard benchmark matrix for the tiny helper lane is documented.
- The current evidence gaps are explicit.
- The handoff and roadmap docs point to the benchmark status.
- Validation passes.

## Out of Scope

- Large benchmark runs on heavyweight teacher models.
- Hugging Face publication.
- Adapter training.
- New model search.
