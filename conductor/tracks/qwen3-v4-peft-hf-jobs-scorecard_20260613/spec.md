# Specification: Qwen3 V4 PEFT HF Jobs Scorecard

## Overview

Prepare Hugging Face Jobs as the persistent cloud execution route for the Qwen3
v4 PEFT no-limit selected-task `lm_eval[hf]` scorecard.

## Acceptance Criteria

- Publish or verify a Hub-hosted PEFT adapter artifact that HF Jobs can mount.
- Add a no-limit HF Jobs config that uses the mounted adapter path.
- Keep paid GPU submission approval-gated.
- Record the exact observed hardware/cost options and candidate command.
- Do not claim full benchmark coverage until a submitted job completes all five
  tasks without `--limit`.

## Out Of Scope

- Submitting paid GPU jobs without explicit approval.
- Changing the selected task set.
- Replacing the original MLX adapter release.
