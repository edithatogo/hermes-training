# Colab T4 Smoke: colab-t4-smoke-20260611

Date: 2026-06-11
Status: `scored`

## Runtime

| Field | Value |
|---|---|
| CLI | `colab 0.5.9` |
| Command | `colab run --gpu T4 --timeout 120 scripts/colab_smoke.py` |
| Session | `run-90f315` |
| Requested accelerator | `T4` |
| Observed accelerator | `Tesla T4` |
| Python | `3.12.13` |
| Torch | `2.11.0+cu128` |
| CUDA available | `true` |
| CUDA capability | `7.5` |
| Session cleanup | `terminated` |

## Artifacts

| Field | Value |
|---|---|
| SSD log | `/Volumes/PortableSSD/hermes-evals/colab/colab-t4-smoke-20260611/colab-run.log` |
| Script | `scripts/colab_smoke.py` |

## Decision

Colab CLI can allocate and run a T4 CUDA runtime from this machine/account.
This is suitable for bounded benchmark smoke and candidate-pilot jobs when
artifacts are copied back to the SSD. It is not Mac/MLX runtime evidence.
