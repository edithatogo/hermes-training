# Specification: Qwen3 v4 Official Candidate Execution Matrix

## Overview

Create a single execution matrix for the Qwen3 v4 Hermes PEFT official-candidate
benchmark slices. The matrix consolidates the official BFCL, coding,
safety/refusal, and RULER readiness gates so the repo has one fail-closed source
of truth for what can run now and what still blocks scored benchmark evidence.

## Goals

- Read the existing official-candidate suite queue.
- Pull current execution status from the BFCL, coding, safety/refusal, and RULER
  setup reports.
- Keep all large benchmark outputs on `/Volumes/PortableSSD`.
- Preserve the publication boundary: no broad benchmark claim until each
  required suite has scored artifacts or an explicit exclusion.
- Wire the matrix into hub readiness so stale or missing matrix reports fail.

## Acceptance Criteria

- Add `scripts/build_official_candidate_execution_matrix.py`.
- Add `scripts/validate_official_candidate_execution_matrix.py`.
- Generate JSON and Markdown matrix reports under
  `reports/benchmark/official-candidates/`.
- Add focused unit tests for blocked/ready suite status and the publication
  boundary.
- Wire the matrix validator into `scripts/validate_readiness.py`.
- Add this Conductor track and keep registry consistency green.

## Out Of Scope

- Running BFCL, EvalPlus, safety/refusal runtime scoring, or RULER.
- Installing missing benchmark packages.
- Starting local endpoints or cloud compute.
- Claiming official benchmark scores.
