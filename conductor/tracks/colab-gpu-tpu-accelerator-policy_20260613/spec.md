# Specification: Colab GPU/TPU Accelerator Policy

## Problem

The Colab dispatcher already had a TPU-aware accelerator list, but the cloud
preflight and unblock checklist still described Colab as GPU-first only. That
made the operational plan ambiguous: TPU should be available for compatible
adaptive smokes, but PEFT lm-eval, MLX scoring, and llama.cpp/GGUF endpoint
pilots should not be routed to TPU.

## Scope

- Add an explicit Colab accelerator policy to the cloud backend preflight.
- Surface the policy in the unblock checklist and active blocked-track matrix.
- Keep TPU opt-in through `--allow-tpu`.
- Add tests covering the policy and the full GPU/TPU ladder.

## Out Of Scope

- No live Colab runtime creation.
- No benchmark execution or scorecard claim.
- No change to the blocked no-limit Colab scorecard status.

## Acceptance Criteria

- `reports/cloud/backend-preflight-20260613.*` records the GPU/TPU ladder.
- `reports/cloud/backend-unblock-checklist-20260613.*` tells operators when TPU
  may and may not be used.
- Unit tests and full readiness pass.
- Health remains `>= 9.5 / 10`.
