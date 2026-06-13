# Specification: Qwen3 V4 Full Selected-Task Scorecard Execution

## Overview

Run the no-limit selected-task `lm-eval` scorecard for the Qwen3 v4 strict Hermes tool-call adapter through the direct MLX loglikelihood adapter.

## Goals

- Execute the plan in `reports/benchmark/manifests/lm-eval-full-scorecard-plan-20260613.yaml`.
- Keep all raw outputs under `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613`.
- Produce or resume `summary.json`, `results.json`, and `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613.md`.
- Update the standard coverage report only if every selected task is scored.

## Acceptance Criteria

- The run completes with `summary.json` status `scored`, or records a concrete blocker without losing partial task artifacts.
- `results.json` contains all selected tasks before any full-scorecard claim is made.
- Repository validation passes after reports are updated.
- Public benchmark claims remain blocked unless the coverage report no longer marks `lm-eval-selected` missing.

## Out Of Scope

- Publishing benchmark results to Hugging Face or GitHub releases.
- Running official BFCL, coding, safety, or RULER suites in this track.
- Changing Hermes model selection before the full run is scored and reviewed.
