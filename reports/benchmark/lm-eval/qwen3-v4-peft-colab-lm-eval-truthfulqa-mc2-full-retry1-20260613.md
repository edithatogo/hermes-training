# Qwen3 V4 PEFT Colab TruthfulQA MC2 Full Shard Retry 1

Run ID: `qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry1`

## Summary

Status: `blocked-pruned`

The `truthfulqa_mc2` no-limit shard was launched on a Google Colab T4 session
using the checkpoint-enabled PEFT lm-eval runner version that emitted
pre-evaluation checkpoints only. The session reached dependency install,
adapter upload, adapter extraction, and the `adapter-ready` checkpoint. Repeated
recovery polls showed the downloaded result JSON never advanced beyond
`adapter-ready`, no harness result files were visible under the output
directory, and the next `colab status` call pruned the stale local session.

This is not scorecard evidence. It is recovery evidence that retry1 reached the
adapter-ready boundary but did not produce recoverable evaluation results under
the current Colab keepalive permission blocker.

## Attempt

| Field | Value |
| --- | --- |
| Backend | Google Colab CLI |
| Session | `qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry1` |
| Accelerator | `Tesla T4` |
| Task | `truthfulqa_mc2` |
| Config | `reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-config-20260613.json` |
| Output root | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry1` |
| Local exec log | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry1/colab-exec.log` |
| Recovered checkpoint JSON | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry1/recovered/summary.json` |
| Latest checkpoint | `adapter-ready` at `2026-06-13T05:01:55.699257+00:00` |
| Latest recovery poll | `2026-06-13T05:10:55.641255+00:00` |
| Final status poll | `colab status` pruned 1 stale local session and reported session not found |
| Wrapper recovery report | `reports/colab/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry1.md` |
| Harness result | not produced/recovered |

## Recovered Checkpoint

The latest downloaded JSON reports:

- `status`: `blocked`
- `checkpoint_phase`: `adapter-ready`
- `tasks`: `truthfulqa_mc2`
- `limit`: `null`
- `cuda_available`: `true`
- `cuda_device_name`: `Tesla T4`
- `accelerate_install.returncode`: `0`
- `install.returncode`: `0`
- `evaluation`: not present
- `result_files`: not present

The `blocked` status is the pre-evaluation default written before the
evaluation subprocess starts. It should not be interpreted as a final task
failure unless the session ends without an `evaluation-complete` checkpoint.

## Blocker

`colab log` shows the keepalive helper failed twice with HTTP 403 for project
`1014160490159`:

`Caller does not have required permission to use project 1014160490159. Grant
the caller the roles/serviceusage.serviceUsageConsumer role, or a custom role
with the serviceusage.services.use permission`

The keepalive helper stopped after consecutive 4xx failures. The kernel may
still finish, but this is the same account/project condition that caused the
previous no-limit Colab attempts to lose recoverable artifacts.

## Decision

Retry1 is closed as blocked/pruned. Future Colab retries should use the
heartbeat-enabled runner from commit `6fb806e` and the shard wrapper from commit
`9487c69`, so an in-flight evaluation can emit `evaluation-running` checkpoints
before Colab pruning loses the session. Keep public no-limit scorecard claims
blocked until a shard produces an `evaluation-complete` checkpoint and
downloadable lm-eval output.
