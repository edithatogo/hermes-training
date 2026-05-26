# Specification: MLX Direct lm-eval Candidate Scorecard

Convert the direct MLX `lm_eval` adapter from smoke-only evidence into a
bounded candidate scorecard for the current Qwen3 v4 strict Hermes tool-call
adapter.

Acceptance criteria:

- Run the selected official `lm_eval` task set through `scripts/run_mlx_lm_eval.py`
  with a larger fixed sample limit than the existing limit-10 smoke.
- Store all generated benchmark artifacts under the SSD-backed
  `/Volumes/PortableSSD/hermes-evals` root.
- Track the generated run card under `reports/benchmark/lm-eval/`.
- Update standard benchmark coverage so the limit-25 run is visible as a
  candidate-pilot scorecard, while still avoiding leaderboard/full-task claims.
- Update the handoff notes so the next benchmark step moves from "first broader
  selected-task run" to "increase sample/full-run coverage or add missing suites".
- Keep public release gating honest: this scorecard may improve evidence, but it
  must not unblock public dataset/model release approval by itself.
