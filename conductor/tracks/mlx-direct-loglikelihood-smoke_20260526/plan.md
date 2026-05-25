# Plan: MLX Direct Loglikelihood Smoke Harness

## Phase 1: Direct Scorer

- [x] Task: add `scripts/run_mlx_loglikelihood_smoke.py`.
- [x] Task: add `scripts/run_mlx_lm_eval.py` as a direct `lm_eval`
  loglikelihood adapter scaffold.
- [x] Task: add a tiny prompt/continuation JSONL suite.
- [x] Task: implement a no-download mock scoring mode for validation.
- [x] Task: cover parsing, continuation alignment, mock scoring, adapter
  self-test, dry-run, and output schema in tests.

## Phase 2: Evidence and Coverage

- [x] Task: run the mock schema smoke under `/Volumes/PortableSSD/hermes-evals`.
- [x] Task: add a tracked benchmark report for the direct harness.
- [x] Task: update standard benchmark coverage to list the harness as
  diagnostic, while keeping `lm-eval-selected` blocked for real scores.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: direct scorer and adapter scaffold code/tests exist; the mock
  schema smoke produced SSD-backed summary/results artifacts; coverage no
  longer treats the next loglikelihood path as undocumented.
- Remaining gap: the Qwen3 v4 adapter still needs a non-mock direct MLX run
  against selected task documents before any official benchmark score claim.
