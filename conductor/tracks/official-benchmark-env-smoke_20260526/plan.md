# Plan: Official Benchmark Environment Smoke

## Phase 1: Smoke Harness

- [x] Task: add `scripts/smoke_official_benchmark_env.py`.
- [x] Task: add unit coverage for mode definitions and missing package handling.
- [x] Task: include the script in structural readiness syntax checks.

## Phase 2: Live Environment Verification

- [x] Task: run the general benchmark environment smoke from
  `/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312`.
- [x] Task: run the BFCL environment smoke from
  `/Volumes/PortableSSD/hermes-training-envs/bfcl-py312`.
- [x] Task: store generated JSON outputs under
  `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/env-smoke`.

## Phase 3: Documentation

- [x] Task: record a dated smoke report.
- [x] Task: link the smoke report from `STANDARD_BENCHMARKS.md`.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: both isolated environments smoke-tested, generated artifacts remain
  on SSD, and validation passes.
- Gaps: this proves harness readiness only; official BFCL, IFEval, lm-eval,
  HumanEval, EvalPlus, and MTEB benchmark scores still require separate runs.
- Decision: complete this track as benchmark infrastructure verification.
