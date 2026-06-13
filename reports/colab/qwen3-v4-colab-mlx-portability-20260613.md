# Colab Dispatch: qwen3-v4-colab-mlx-portability-20260613

Date: 2026-06-13T02:04:32.301908+00:00
Status: `blocked`
Script: `scripts/colab_mlx_adapter_portability_probe.py`
Output: `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-colab-mlx-portability-20260613`

## Attempts

| Accelerator | Status | Duration | Log | Observed |
|---|---|---:|---|---|
| `gpu:T4` | `blocked` | 42.096s | `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-colab-mlx-portability-20260613/gpu-T4.log` | cuda_device_name=Tesla T4, cuda_available=true, script_status=blocked, script_decision=The published adapter is visible, but the MLX adapter path is not a CUDA/T4 lm-eval path; use a PEFT/fused artifact or a Mac/MLX runner. |

## Decision

Probe executed on Colab T4, but the emitted probe status is blocked: the public adapter is visible and CUDA is available, while the MLX adapter path is not a CUDA/T4 lm-eval route. Produce a PEFT/fused artifact or keep the scorecard on a Mac/MLX runner.
