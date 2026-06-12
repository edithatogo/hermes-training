# MiniCPM5 1B MLX Strict BFCL Pilot

Run ID: `minicpm5-1b-mlx-strict-bfcl-pilot-20260613`
Created: 2026-06-12T14:35:45.413128+00:00
Model: `openbmb/MiniCPM5-1B-MLX`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, offline SSD cache, no assistant prefill, no score wrapper
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/minicpm5-1b-mlx-strict-bfcl-pilot-20260613`

## Command

```bash
source scripts/env.sh
HF_HUB_OFFLINE=1 ./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model openbmb/MiniCPM5-1B-MLX \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id minicpm5-1b-mlx-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

MiniCPM5 loaded quickly from the SSD cache, but every strict case failed. The
successful-tool cases produced reasoning text and argument fragments rather than
Hermes tool-call objects. The invalid-tool case hallucinated that
`delete_customer_record` was available and then emitted tool-like text, so it
failed both availability handling and the no-extra-tool-text gate.

## Decision

Keep `openbmb/MiniCPM5-1B-MLX` as a tiny helper/runtime candidate only. It is
not suitable for strict Hermes tool-calling without prompt-profile repair or a
targeted fine-tune.
