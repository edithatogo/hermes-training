# Gemma 4 E2B MLX 4-bit Load Failure - 2026-06-13

## Summary

`mlx-community/gemma-4-e2b-it-4bit` was acquired to the SSD-backed Hugging Face
cache and then tested through the local MLX pilot harness.

The model did not reach generation or benchmarking. Current `mlx_lm` failed
during weight loading because the repository contains attention-layer
parameters that are not present in the instantiated model definition.

## Artifact

- Repo: `mlx-community/gemma-4-e2b-it-4bit`
- Snapshot:
  `/Volumes/PortableSSD/huggingface/hub/models--mlx-community--gemma-4-e2b-it-4bit/snapshots/2c3e507453b4f218d05fe3cc97bea5c5a654257e`
- Cache size: `3.4G`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`

## Runtime

- `mlx_lm`: `0.31.3`
- Harness: `scripts/run_local_pilot_benchmark.py`
- Suite requested: `benchmarks/endpoint_pilots/bfcl_pilot.json`
- Run id requested: `gemma4-e2b-mlx-4bit-strict-bfcl-pilot-20260613`

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model mlx-community/gemma-4-e2b-it-4bit \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id gemma4-e2b-mlx-4bit-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

## Failure

The model downloaded successfully, then `mlx_lm.load()` failed before generation:

```text
ValueError: Received 140 parameters not in model
```

The extra parameters were concentrated in
`language_model.model.layers.15` through `language_model.model.layers.34`
self-attention weights, including `k_norm`, `k_proj`, and `v_proj` tensors.

## Decision

- Status: `acquired; mlx-load-blocked`
- Do not promote or benchmark this package until `mlx_lm` supports the current
  Gemma 4 E2B MLX checkpoint layout or the model package is revised.
- Keep the cached artifact on the SSD for a future runtime retry, because the
  download completed and the model is small enough for the Mac runtime lane.
