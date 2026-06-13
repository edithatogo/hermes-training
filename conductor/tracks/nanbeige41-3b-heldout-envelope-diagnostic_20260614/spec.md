# Specification: Nanbeige 4.1 3B Held-Out Envelope Diagnostic

## Overview

The first Nanbeige constrained-envelope replay passed the three-case pilot, but
promotion requires held-out evidence. This track records the held-out replay
result and keeps the boundary explicit.

## Scope

- Use existing held-out strict outputs from
  `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/nanbeige41-3b-heldout-strict-20260614`.
- Replay through the deterministic constrained-envelope diagnostic.
- Track compact JSON and Markdown reports under
  `reports/benchmark/constrained-envelope/`.
- Validate that the report is non-promotional and not represented as a pass.

## Out Of Scope

- No model rerun.
- No training.
- No cloud job.
- No raw-output promotion.
- No default routing change.

## Decision

The held-out replay improved Nanbeige from raw `1/8` to constrained `3/8`, but
the result remains below promotion threshold. Treat it as wrapper-design
evidence only.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: readiness validates the report, source output directory, full replay
  artifacts, and non-promotion boundary.
- Remaining gap: a real runtime-wrapper proof must pass broader held-out suites.
