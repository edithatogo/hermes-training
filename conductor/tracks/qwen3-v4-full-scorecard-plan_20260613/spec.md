# Specification: Qwen3 V4 Full Scorecard Plan

## Overview

Create a first-class, validator-enforced execution plan for the Qwen3 v4 full selected-task `lm-eval` scorecard. This closes the handoff ambiguity between the completed `--limit 10` and `--limit 25` pilots and the still-missing full selected-task benchmark.

## Goals

- Define the exact full selected-task run ID, tasks, model, adapter, output directory, and report path.
- Keep all raw benchmark outputs under `/Volumes/PortableSSD/hermes-evals/standard-benchmarks`.
- Preserve the current publication boundary: this is an internal candidate scorecard until the full run completes and the coverage report is regenerated.
- Add automated validation so future edits cannot silently reintroduce a sample limit or off-SSD output path.

## Acceptance Criteria

- Add a machine-readable scorecard plan under `reports/benchmark/manifests/`.
- Add a human-readable companion plan with the exact command and guardrails.
- Extend `scripts/validate_official_benchmark_manifests.py` to validate the full scorecard plan.
- Add unit coverage for the validator.
- Keep the track health estimate at or above 9.5 with passing readiness validation.

## Out Of Scope

- Launching the full benchmark in this track.
- Publishing model, adapter, dataset, or benchmark artifacts.
- Changing the current best-model decision before a scored full run exists.
