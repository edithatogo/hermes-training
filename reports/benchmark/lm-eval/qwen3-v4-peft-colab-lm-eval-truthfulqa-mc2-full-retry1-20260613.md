# Qwen3 V4 PEFT Colab TruthfulQA MC2 Full Shard Retry 1

Run ID: `qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry1`

## Summary

Status: `in-progress-at-risk`

The `truthfulqa_mc2` no-limit shard was launched on a Google Colab T4 session
using the checkpoint-enabled PEFT lm-eval runner. The session reached
dependency install, adapter upload, adapter extraction, and the `adapter-ready`
checkpoint. At the latest recovery poll, `colab status` still reported the
kernel as `BUSY (exec(scripts/colab_peft_lm_eval_selected.py))`, but the
downloaded result JSON had not advanced beyond `adapter-ready` and no harness
result files were visible under the output directory.

This is not scorecard evidence yet. It is recovery evidence that the retry is
alive enough to download checkpoints, while the same Colab keepalive permission
blocker remains present.

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

Do not launch another no-limit Colab shard while this retry is active. Poll and
recover this session first. If it completes with an `evaluation-complete`
checkpoint, download the result JSON plus the lm-eval output directory and
update the shard track. If it is pruned or remains stuck without result files,
keep the Colab shard lane blocked until the Google Cloud service-usage
permission or an external persistent-artifact backend is fixed.
