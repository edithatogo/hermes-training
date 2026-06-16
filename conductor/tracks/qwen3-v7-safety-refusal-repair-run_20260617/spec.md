# Specification: Qwen3 v7 Safety/Refusal Repair Run

## Overview

Run the bounded Qwen3 v7 safety/refusal repair fine-tune locally, rerun the
pinned safety/refusal suite, and ingest compact result evidence while keeping
weights and raw outputs out of git.

## Goals

- Train the v7 MLX LoRA adapter from the v7 repair dataset.
- Keep adapter weights under ignored `gemma4/experiments/`.
- Rerun the pinned 8-case safety/refusal suite against the v7 adapter.
- Store raw benchmark outputs under `/Volumes/PortableSSD`.
- Add a compact repo report comparing v4 baseline and v7 repair results.
- Keep publication blocked unless all target gates are met.

## Acceptance Criteria

- Training completes with the v7 config and writes an ignored adapter.
- Safety/refusal rerun writes SSD-backed raw artifacts.
- Add `scripts/build_safety_refusal_repair_run_report.py`.
- Add `scripts/validate_safety_refusal_repair_run_report.py`.
- Generate JSON and Markdown repair-run reports under
  `reports/benchmark/official-candidates/`.
- Add focused unit tests.
- Wire validation into `scripts/validate_readiness.py`.
- Add this Conductor track to the registry.

## Out Of Scope

- Publishing the v7 adapter.
- Pushing model weights to GitHub.
- Claiming safety/refusal readiness.
- Running standardized external safety suites.
