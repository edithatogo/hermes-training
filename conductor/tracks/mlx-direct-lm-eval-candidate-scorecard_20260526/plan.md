# Plan: MLX Direct lm-eval Candidate Scorecard

## Phase 1: Candidate Run

- [x] Task: run selected `lm_eval` tasks with `--limit 25` through the direct
  MLX adapter.
- [x] Task: verify the run writes `summary.json` and `results.json` under
  `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/`.
- [x] Task: record the markdown run card under `reports/benchmark/lm-eval/`.

## Phase 2: Coverage and Handoff

- [x] Task: update standard benchmark coverage to include the limit-25
  candidate-pilot evidence separately from the limit-10 smoke.
- [x] Task: refresh the generated standard coverage report.
- [x] Task: update `HANDOFF.md` and the model radar notes with the scorecard
  interpretation and remaining benchmark gaps.

## Phase 3: Validation

- [x] Task: run focused unit tests for the direct MLX adapter and coverage gate.
- [x] Task: run repository readiness checks without writing model artifacts to
  the internal disk.
- [x] Task: commit and push the completed track.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: the direct MLX adapter scored selected ARC Challenge, HellaSwag,
  TruthfulQA MC2, GSM8K, and Winogrande at `--limit 25`; SSD summary/results
  artifacts and a tracked run card exist; standard coverage now distinguishes
  limit-10 smoke from limit-25 candidate-pilot evidence.
- Remaining gap: this is still bounded sample evidence. Full selected-task
  `lm_eval`, official BFCL, official coding, safety/refusal, and RULER suites
  remain missing for broad benchmark claims.
