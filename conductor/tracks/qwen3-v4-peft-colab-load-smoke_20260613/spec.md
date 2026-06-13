# Specification: Qwen3 V4 PEFT Colab Load Smoke

## Overview

Use Colab T4 to test whether the converted Qwen3 v4 PEFT candidate can load with `Qwen/Qwen3-4B` under Transformers/PEFT.

## Acceptance Criteria

- Upload the converted PEFT candidate tarball to a Colab T4 session.
- Execute `scripts/colab_peft_adapter_load_smoke.py`.
- Record a tracked report with either load/generation success or a concrete blocker.
- Do not run or claim full selected-task `lm-eval` until this load smoke passes.

## Out Of Scope

- Hugging Face publication.
- Full benchmark scoring.
- Long-running training.
