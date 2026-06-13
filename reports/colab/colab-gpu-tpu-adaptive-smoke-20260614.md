# Colab Dispatch: colab-gpu-tpu-adaptive-smoke-20260614

Date: 2026-06-13T17:44:46.271148+00:00
Status: `scored`
Script: `scripts/colab_adaptive_train_smoke.py`
Output: `/Volumes/PortableSSD/hermes-evals/colab/colab-gpu-tpu-adaptive-smoke-20260614`

## Attempts

| Accelerator | Status | Duration | Log | Observed |
|---|---|---:|---|---|
| `gpu:T4` | `blocked` | 51.520s | `/Volumes/PortableSSD/hermes-evals/colab/colab-gpu-tpu-adaptive-smoke-20260614/gpu-T4.log` | none |
| `gpu:L4` | `blocked` | 2.152s | `/Volumes/PortableSSD/hermes-evals/colab/colab-gpu-tpu-adaptive-smoke-20260614/gpu-L4.log` | none |
| `gpu:A100` | `blocked` | 1.950s | `/Volumes/PortableSSD/hermes-evals/colab/colab-gpu-tpu-adaptive-smoke-20260614/gpu-A100.log` | none |
| `tpu:v5e1` | `scored` | 43.459s | `/Volumes/PortableSSD/hermes-evals/colab/colab-gpu-tpu-adaptive-smoke-20260614/tpu-v5e1.log` | training_backend=xla, training_device_name=xla:0 |

## Decision

First available accelerator completed successfully.
