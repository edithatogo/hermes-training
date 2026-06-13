# Plan: Qwen3 V4 Full Scorecard Plan

## Phase 1 - Execution Manifest

- [x] Task: Add the full selected-task scorecard plan.
  - [x] Record run ID, model, adapter, task list, batch size, max length, output root, and report path.
  - [x] Require `limit: null` and omit `--limit` from the command.
  - [x] Keep large outputs under `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/`.

## Phase 2 - Validation

- [x] Task: Extend official benchmark manifest validation.
  - [x] Validate the YAML plan shape and exact candidate identity.
  - [x] Reject off-SSD artifact roots and output paths.
  - [x] Reject full-scorecard plans that include a sample limit.
- [x] Task: Add unit tests for the scorecard-plan validator.

## Phase 3 - Documentation And Handoff

- [x] Task: Link the new plan from the benchmark manifests.
- [x] Task: Preserve the non-publication boundary until the run is complete.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: `reports/benchmark/manifests/lm-eval-full-scorecard-plan-20260613.yaml` and `.md` define the exact full selected-task scorecard path; `scripts/validate_official_benchmark_manifests.py` now validates that it is full-run, SSD-backed, and internal-candidate only.
- Validation: `scripts/validate_official_benchmark_manifests.py`, focused unit tests, and hub readiness validation are required before commit.
- Gaps: The full benchmark is still intentionally not run in this track.
- Decision: Complete. The track improves execution readiness without making a benchmark claim.
