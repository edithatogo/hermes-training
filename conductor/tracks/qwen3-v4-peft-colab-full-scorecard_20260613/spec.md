# Specification: Qwen3 V4 PEFT Colab Full Scorecard

## Overview

Run the no-limit selected-task `lm-eval` scorecard for the converted Qwen3 v4
PEFT candidate through the validated Colab T4 + Hugging Face PEFT route.

## Acceptance Criteria

- Use `scripts/colab_peft_lm_eval_selected.py` with the full-scorecard config
  in `reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-selected-full-config-20260613.json`.
- Upload the converted PEFT adapter tarball and config to a clean Colab T4
  session.
- Download the run JSON and harness result file to
  `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-lm-eval-selected-full-20260613`.
- Record a tracked benchmark report with task metrics, wall-clock runtime,
  session cleanup state, and any blocker.
- Do not update public benchmark claims unless all five selected tasks complete
  without `--limit`.

## Out Of Scope

- Changing the selected task set.
- Publishing the converted adapter.
- Treating bounded pilot scores as no-limit coverage.
