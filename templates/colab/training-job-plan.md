# Colab Training Job Plan: <run-id>

Use this template before running `scripts/colab_dispatch.py` for training or
fine-tuning work.

## Compatibility

| Field | Value |
|---|---|
| Script | `<path>` |
| Model | `<model id>` |
| Dataset | `<dataset or benchmark>` |
| CUDA path tested | `<yes|no>` |
| TPU/XLA path tested | `<yes|no>` |
| Can include TPU in dispatcher | `<yes|no>` |

## Dispatcher

CUDA-only default:

```bash
./.venv/bin/python scripts/colab_dispatch.py \
  --accelerators gpu:T4,gpu:L4,gpu:A100 \
  --timeout 1800 \
  --run-id <run-id> \
  <script> <args>
```

CUDA or TPU/XLA:

```bash
./.venv/bin/python scripts/colab_dispatch.py \
  --allow-tpu \
  --accelerators gpu:T4,gpu:L4,tpu:v5e1,tpu:v6e1,gpu:A100 \
  --timeout 1800 \
  --run-id <run-id> \
  <script> <args>
```

## Artifact Policy

- Remote checkpoint path:
- SSD checkpoint path:
- SSD metrics path:
- Tracked report path:

Stop and mark blocked if the run cannot sync artifacts back to the SSD.
