# Qwen3 V4 PEFT NGC Cloud Function Discovery

Status: `blocked-needs-ngc-config-and-container`

## Current CLI State

`ngc config current` shows only the default output format:

```text
format_type = ascii
```

No API key, org, or team is configured.

## Execution Surface Observed

The installed NGC CLI does not expose `ngc batch`. It does expose:

- `ngc registry ...` for registry assets.
- `ngc cloud-function task create ...` for task execution.
- `ngc cloud-function function create ...` and deployment commands.
- `ngc cloud-function gpu quota|list|capacity` for GPU availability checks.
- `ngc sso login` for browser-based login.

The likely task route, after auth and entitlement, is:

```bash
ngc cloud-function task create \
  --name qwen3-v4-peft-lm-eval-selected-full \
  --gpu-specification <gpu:instance_type[:backend][:cluster]> \
  --container-image <org>/<team>/<image>:<tag> \
  --container-environment-variable RUN_ID:qwen3-v4-peft-ngc-lm-eval-selected-full-20260613 \
  --container-environment-variable PEFT_ADAPTER_REPO:edithatogo/qwen3-4b-hermes-lora-peft-converted \
  --container-environment-variable LM_EVAL_TASKS:arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande \
  --max-runtime-duration 6H \
  --result-handling-strategy UPLOAD
```

## Blockers

- NGC API key or SSO login is not configured.
- NGC org/team and entitlement are unknown.
- GPU quota/capacity is unknown.
- No NGC registry container image exists for the benchmark runner.
- Result storage location and retrieval flow are not proven.

## Decision

Keep NGC as a prepared discovery lane only. Do not add live commands until auth,
org/team, GPU quota, container registry, and result persistence are proven.
