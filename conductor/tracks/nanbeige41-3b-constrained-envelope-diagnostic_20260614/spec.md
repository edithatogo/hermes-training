# Specification: Nanbeige 4.1 3B Constrained Envelope Diagnostic

## Overview

Nanbeige 4.1 3B produced exact Hermes tool-call payloads in the strict BFCL pilot
but wrapped them in reasoning text, causing the raw strict run to score `0/3`.
This track implements a deterministic constrained-envelope replay diagnostic
against the existing SSD-backed responses.

## Scope

- Add a reusable constrained-envelope replay script.
- Strip reasoning only by selecting model-generated tool calls or a safe
  model-generated refusal sentence.
- Score the constrained replay with strict `--require-no-extra-tool-text`.
- Track a compact report while keeping full replay artifacts on the SSD.

## Out Of Scope

- No model rerun.
- No training.
- No cloud job.
- No raw-output promotion.
- No Hermes default model switch.

## Acceptance Criteria

- The raw Nanbeige strict baseline remains recorded as `0/3`.
- The constrained-envelope replay produces `3/3` on the 3-case diagnostic suite.
- The report explicitly sets `promotion_allowed=false`.
- Full readiness validates the tracked report and SSD-backed source artifacts.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.8 / 10`
- Evidence: the diagnostic is deterministic, source-backed, strict-scored, and
  guarded by unit tests plus readiness validation.
- Remaining gap: this is not a live runtime-wrapper proof across held-out suites.
