# Qwen3 V4 PEFT Colab lm-eval Full Scorecard Attempt

Run ID: `qwen3-v4-peft-lm-eval-selected-full-20260613`

## Summary

Status: `blocked`

The no-limit selected-task `lm_eval[hf]` scorecard was launched on a clean
Google Colab T4 session using the validated converted PEFT route. The run
reached adapter extraction and entered the no-limit harness execution phase, but
the Colab session was pruned before any result JSON or harness result file could
be recovered.

This does not invalidate the PEFT route. The bounded pilot in
`reports/benchmark/lm-eval/qwen3-v4-peft-colab-lm-eval-selected-limit5-20260613.md`
scored through the same adapter, dependency pin, quantization path, and task
set. The blocker is long-running Colab session stability under the current
`google-colab-cli` account/project keepalive permissions.

## Attempt

| Field | Value |
| --- | --- |
| Backend | Google Colab CLI |
| Session | `qwen3-v4-peft-lmeval-full-20260613` |
| Accelerator | `Tesla T4` |
| Config | `reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-selected-full-config-20260613.json` |
| Adapter tarball | `/content/qwen3-v4-peft-conversion-20260613.tar.gz` |
| Config path on Colab | `/content/qwen3-v4-peft-lm-eval-config.json` |
| Output root | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-lm-eval-selected-full-20260613` |
| Local wrapper log | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-lm-eval-selected-full-20260613/colab-exec-full.log` |
| Result JSON | not produced/recovered |
| Harness result | not produced/recovered |
| Cleanup | `colab sessions` reported no active sessions after pruning |

## Blocker

`colab log` showed the session keepalive helper failing twice with HTTP 403:

`Caller does not have required permission to use project 1014160490159. Grant
the caller the roles/serviceusage.serviceUsageConsumer role, or a custom role
with the serviceusage.services.use permission`

After roughly the first long polling window, `colab status -s
qwen3-v4-peft-lmeval-full-20260613` pruned the local session and reported that
the session was not found. The local `colab exec` wrapper remained attached but
never emitted a final JSON result, so it was interrupted to avoid an indefinite
hang.

## Decision

Keep `lm-eval-selected` full coverage blocked. The next retry should use one of:

- Fix Colab keepalive permissions for project `1014160490159`, then rerun the
  same config.
- Use a Colab/Drive or HF Job workflow that writes incremental artifacts outside
  the live kernel before session pruning can lose state.
- Move the no-limit scorecard to Azure/NVIDIA/HF Jobs with persistent storage.

Do not promote public no-limit benchmark claims from this attempt.
