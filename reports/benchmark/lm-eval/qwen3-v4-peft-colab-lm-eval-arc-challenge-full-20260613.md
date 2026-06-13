# Qwen3 V4 PEFT Colab ARC Challenge Full Shard Attempt

Run ID: `qwen3-v4-peft-lm-eval-arc-challenge-full-20260613`

## Summary

Status: `blocked`

The `arc_challenge` no-limit shard was launched on a clean Google Colab T4
session using the validated Qwen3 v4 PEFT route. The run reached adapter
extraction and entered harness execution, but the Colab session was pruned
before any JSON or harness result artifact could be recovered.

This shows that task sharding alone is not enough under the current Colab
account/project state. The keepalive permission issue must be fixed, or the
full scorecard must move to a backend with persistent job storage.

## Attempt

| Field | Value |
| --- | --- |
| Backend | Google Colab CLI |
| Session | `qwen3-v4-peft-arc-full-20260613` |
| Accelerator | `Tesla T4` |
| Task | `arc_challenge` |
| Config | `reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-arc-challenge-full-config-20260613.json` |
| Output root | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-lm-eval-arc-challenge-full-20260613` |
| Local wrapper log | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-lm-eval-arc-challenge-full-20260613/colab-exec-arc.log` |
| Result JSON | not produced/recovered |
| Harness result | not produced/recovered |
| Cleanup | `colab sessions` reported no active sessions after pruning |

## Blocker

`colab log` again showed HTTP 403 keepalive failures for project
`1014160490159`, requiring `roles/serviceusage.serviceUsageConsumer` or an
equivalent `serviceusage.services.use` permission. After the keepalive helper
stopped, the session was later pruned while the wrapper was still attached.

## Decision

Pause no-limit Colab shard execution. Continue with one of:

- Fix the Google Cloud service usage permission behind `google-colab-cli`.
- Use a persistent backend such as Azure, NVIDIA/NGC, Kaggle, or Hugging Face
  Jobs.
- Rework Colab execution to write progress to mounted Drive or another external
  store before long kernels are pruned.
