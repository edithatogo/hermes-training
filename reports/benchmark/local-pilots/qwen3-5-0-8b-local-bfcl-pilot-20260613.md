# Qwen3.5 0.8B Strict BFCL Pilot

Run ID: `qwen3-5-0-8b-local-bfcl-pilot-20260613`
Created: 2026-06-12T14:29:16.050887+00:00
Model: `Qwen/Qwen3.5-0.8B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, offline SSD cache, no assistant prefill, no score wrapper
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-5-0-8b-local-bfcl-pilot-20260613`

## Command

```bash
source scripts/env.sh
HF_HUB_OFFLINE=1 ./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model Qwen/Qwen3.5-0.8B \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id qwen3-5-0-8b-local-bfcl-pilot-20260613 \
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

The model loaded from the SSD cache and generated responses, but every strict
case failed. It emitted reasoning text and malformed or incomplete tool-call
fragments instead of exact Hermes tool-call JSON. The invalid-tool case correctly
recognized that the requested tool was unavailable, but still included excluded
tool-like text in the answer, so it failed the no-extra-tool-text gate.

## Decision

Keep `Qwen/Qwen3.5-0.8B` blocked for strict Hermes tool-call promotion. It can
remain a tiny helper or prompt-profile research lane, but this offline local
pilot does not support using it as a Hermes tool-calling default.
