# Plan: Qwen3 v4 Safety/Refusal Result Ingest

## Phase 1 - Runtime Execution

- [x] Task: run the pinned safety/refusal suite with the local MLX v4 adapter.
- [x] Task: keep raw outputs on `/Volumes/PortableSSD`.
- [x] Task: record strict and diagnostic scores from `summary.json`.

## Phase 2 - Result Report

- [x] Task: add `scripts/build_safety_refusal_result_report.py`.
- [x] Task: add `scripts/validate_safety_refusal_result_report.py`.
- [x] Task: generate compact JSON and Markdown reports under
  `reports/benchmark/official-candidates/`.
- [x] Task: add focused unit tests for score preservation and claim boundaries.

## Phase 3 - Matrix And Readiness

- [x] Task: update the official-candidate execution matrix to detect the scored
  safety/refusal artifact.
- [x] Task: regenerate the execution matrix.
- [x] Task: wire result validation into `scripts/validate_readiness.py`.
- [x] Task: add this Conductor track to the registry.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: the run completed, raw artifacts are SSD-backed, compact reports are
  validator-backed, focused tests pass, and the execution matrix reflects the
  scored artifact.
- Remaining gap: the score is not a pass. Strict pass rate is 0.125, with
  refusal failures requiring repair and all strict tool-call successes relying
  on diagnostic empty-think stripping.
- Decision: complete this ingest track and open the next work item as refusal
  and empty-think repair, not publication.
