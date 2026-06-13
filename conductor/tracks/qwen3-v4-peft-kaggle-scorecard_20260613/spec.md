# Specification: Qwen3 V4 PEFT Kaggle Scorecard

## Overview

Prepare Kaggle Kernels as an additional persistent cloud execution route for the
Qwen3 v4 PEFT no-limit selected-task `lm_eval[hf]` scorecard.

## Acceptance Criteria

- Add a Kaggle runner that downloads the public PEFT adapter inside the kernel.
- Add a fail-closed submitter that stages `kernel-metadata.json`, config, and
  runner code.
- Keep Kaggle execution confirmation-gated.
- Record the current authentication blocker.
- Do not claim full benchmark coverage until a submitted kernel completes all
  five selected tasks without `--limit`.

## Out Of Scope

- Submitting kernels without explicit confirmation.
- Uploading private data to Kaggle.
- Replacing Colab, HF Jobs, Azure, or NGC as available backend options.
