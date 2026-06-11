# Colab TPU v5e1 Smoke: colab-tpu-v5e1-smoke-20260611

Date: 2026-06-11
Status: `scored`

## Runtime

| Field | Value |
|---|---|
| CLI | `colab 0.5.9` |
| Command | `colab run --tpu v5e1 --timeout 180 scripts/colab_smoke.py` |
| Session | `run-89145d` |
| Requested accelerator | `v5e1` |
| Observed accelerator | `xla:0` |
| Python | `3.12.13` |
| Torch | `2.9.0+cpu` |
| `torch_xla` available | `true` |
| CUDA available | `false` |
| Session cleanup | `terminated` |

## Artifacts

| Field | Value |
|---|---|
| SSD log | `/Volumes/PortableSSD/hermes-evals/colab/colab-tpu-v5e1-smoke-20260611/colab-run.log` |
| Script | `scripts/colab_smoke.py` |

## Decision

Colab CLI can allocate and run a TPU v5e1 runtime from this machine/account.
TPU jobs must use JAX or PyTorch/XLA-compatible code paths; CUDA-only benchmark
or training scripts will not run unchanged on this lane.
