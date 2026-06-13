# Specification: Prompt/Profile Repair Experiments

## Overview

The prompt/profile repair queue identifies which Hermes candidates need local
repair, but future runs also need concrete, repeatable experiment variants. This
track generates those variants from the queue using the existing local and
endpoint pilot runners.

## Goals

- Generate per-candidate repair experiments from the repair queue.
- Keep every command no-download and strict with `--require-no-extra-tool-text`.
- Support system prefix/suffix controls in the local MLX pilot runner, matching
  endpoint pilot controls.
- Mark score-only normalizer variants as analysis-only so they cannot be used
  as raw-output promotion evidence.
- Add deterministic validation and full readiness coverage.

## Acceptance Criteria

- `reports/benchmark/coverage/prompt-profile-repair-experiments-20260614.*`
  exists and is generated deterministically.
- The matrix includes concrete family-specific variants for Qwen, Gemma,
  Granite, MiniCPM, empty-output, and generic strict-suffix repairs.
- Local and endpoint command templates include `--require-no-extra-tool-text`.
- Analysis-only score normalizer variants explicitly block raw-output promotion.
- Focused unit tests, the experiment validator, Conductor consistency, and full
  readiness pass.

## Out Of Scope

- Running the repair experiments.
- Downloading additional model artifacts.
- Promoting any repaired profile as Hermes default.
- Launching cloud or paid compute.
