# Specification: Qwen3 V4 PEFT Colab lm-eval Pilot

## Overview

Run a bounded selected-task `lm-eval` pilot for the converted Qwen3 v4 PEFT candidate on Colab T4.

## Acceptance Criteria

- Add a Colab script that installs `lm_eval[hf]`, extracts the PEFT candidate, and runs the selected task set through the Hugging Face model adapter.
- Use the converted adapter under `/Volumes/PortableSSD/hermes-evals` and upload it to Colab without committing large files.
- Record a tracked report with status, runtime, tasks, limit, and concrete blocker or score-route success.
- Keep claim boundaries explicit: this pilot is not the full no-limit scorecard.

## Out Of Scope

- Full no-limit selected-task scoring.
- Publication of a benchmark claim.
- Publishing the converted adapter to Hugging Face.
