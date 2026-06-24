# Specification: Qwen3 BFCL + Safety Blocker Resolution

## Overview

Create an umbrella execution track that coordinates two active source tracks
without replacing them:

- `qwen3-v4-bfcl-zero-score-repair_20260624`
- `qwen3-v9-runtime-profile-refusal-marker-repair_20260624`

The BFCL lane must convert the current contaminated selected-slice BFCL evidence
into a clean selected-slice regeneration. The safety/refusal lane must train a
bounded v9 repair adapter from the prepared refusal-only rows and rerun the
pinned 8-case suite using the assistant-prefill runtime profile.

## Requirements

- Keep both source tracks active and update them as the owning tracks for their
  respective evidence.
- Keep all raw training, benchmark, and runtime outputs under
  `/Volumes/PortableSSD`.
- Preserve and validate existing dirty BFCL/v9 work rather than reverting it.
- BFCL selected-slice regeneration must use a fresh SSD-backed output root, a
  reachable OpenAI-compatible endpoint, `--num-threads 1`, and preserved
  endpoint/proxy/generate/evaluate logs.
- Safety/refusal rerun must use the v9 adapter path and the pinned suite:
  `reports/benchmark/manifests/safety-refusal-suite-20260616.json`.
- Publication remains blocked unless the relevant gates pass and a separate
  review approves public claims.

## Acceptance Criteria

- Umbrella track artifacts exist and are linked from `conductor/tracks.md`.
- BFCL failure analysis is committed and validates the current stale score as
  contaminated rather than model-quality evidence.
- BFCL clean regeneration records zero upstream-error rows and zero blank-output
  rows before score interpretation.
- v9 repair data/config validate, bounded training completes, and the pinned
  8-case safety/refusal suite is rerun with assistant prefill.
- Reports record strict pass rate, empty-think wrapper count, residual failures,
  and publication boundary.
- GitHub is pushed. Private HF artifact tracking is evidence-only and excludes
  weights unless a later publication review explicitly allows them.

## Out Of Scope

- Replacing the two active source tracks.
- Full official BFCL leaderboard claims.
- Publishing v8 or v9 weights from this track.
- Claiming standardized safety/refusal readiness from the internal 8-case suite.
