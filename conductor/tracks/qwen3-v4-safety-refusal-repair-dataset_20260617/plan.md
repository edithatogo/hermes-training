# Plan: Qwen3 v4 Safety/Refusal Repair Dataset

## Phase 1 - Dataset Materialization

- [x] Task: create the v7 materializer from v6 splits.
- [x] Task: add strict no-wrapper repair rows.
- [x] Task: add refusal rows that avoid echoing unavailable action names.
- [x] Task: add `/no_think` variants for all repair rows.
- [x] Task: materialize train, val, valid, and test splits.

## Phase 2 - Config And Validation

- [x] Task: add the v7 MLX training config.
- [x] Task: add a side-effect-free dataset validator.
- [x] Task: add focused unit tests.
- [x] Task: update `EXPANSION.md`.

## Phase 3 - Readiness

- [x] Task: wire the validator into `scripts/validate_readiness.py`.
- [x] Task: run focused validation.
- [x] Task: run full readiness.
- [x] Task: add this Conductor track to the registry.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: v7 splits are materialized, the config points to a new adapter path,
  validator checks lane counts and contamination boundaries, focused tests pass,
  and full readiness includes the dataset gate.
- Remaining gap: no v7 model has been trained or benchmarked yet.
- Decision: complete this dataset/config track. The next step is a bounded MLX
  repair run followed by the pinned safety/refusal rerun.
