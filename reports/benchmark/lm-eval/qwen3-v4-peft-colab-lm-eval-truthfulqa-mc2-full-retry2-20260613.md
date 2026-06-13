# Qwen3 V4 PEFT Colab TruthfulQA MC2 Full Shard Retry 2

Run ID: `qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry2`

## Summary

Status: `blocked-terminated`

The second `truthfulqa_mc2` no-limit shard retry used the heartbeat-enabled
PEFT lm-eval runner and the shard wrapper. It successfully created a Colab T4
session, uploaded the cleaned PEFT adapter tarball, uploaded the shard config,
entered the runner, and emitted the new `evaluation-running` checkpoint.

The Google Colab keepalive helper still failed with HTTP 403 on project
`1014160490159`, then stopped after consecutive 4xx errors. The Colab session
terminated shortly after the `evaluation-running` checkpoint and before an
`evaluation-complete` checkpoint or lm-eval output directory could be
recovered. The local `colab exec` wrapper remained hung after remote
termination and was interrupted manually; commit after this retry adds a session
watchdog to kill local exec when `colab status` reports the session is gone.

## Attempt

| Field | Value |
| --- | --- |
| Backend | Google Colab CLI |
| Session | `qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry2` |
| Accelerator | `Tesla T4` |
| Task | `truthfulqa_mc2` |
| Config | `reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-config-20260613.json` |
| Output root | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry2` |
| Local exec log | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry2/colab-exec.log` |
| Latest checkpoint | `evaluation-running` |
| Harness result | not produced/recovered |

## Evidence

The local exec log contains:

- `COLAB_LM_EVAL_CHECKPOINT ... "phase": "dependencies-installed", "status": "blocked"`
- `COLAB_LM_EVAL_CHECKPOINT ... "phase": "adapter-ready", "status": "blocked"`
- `COLAB_LM_EVAL_CHECKPOINT ... "phase": "evaluation-running", "status": "running"`

`colab log` for the session recorded:

- session created at `2026-06-13 05:13:07`
- keepalive HTTP 403 at `2026-06-13 05:13:08`
- adapter/config uploads at `2026-06-13 05:13:22` and `2026-06-13 05:13:23`
- second keepalive HTTP 403 at `2026-06-13 05:14:08`
- keepalive stopped after consecutive 4xx errors
- session terminated at `2026-06-13 05:14:48`

## Decision

Retry2 proves the heartbeat checkpoint path works, but it does not produce a
benchmark score. Do not run further no-limit Colab scorecard shards until the
Google Cloud service usage permission issue is fixed, or until the job is moved
to a backend with persistent artifact storage such as Azure, Kaggle, NVIDIA/NGC,
or Hugging Face Jobs.
