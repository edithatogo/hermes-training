# Qwen3.5 2B Strict BFCL Pilot

Run ID: `qwen3-5-2b-local-bfcl-pilot-20260613`
Created: 2026-06-12T14:33:05.665045+00:00
Model: `Qwen/Qwen3.5-2B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, offline SSD cache, no assistant prefill, no score wrapper
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-5-2b-local-bfcl-pilot-20260613`

## Command

```bash
source scripts/env.sh
HF_HUB_OFFLINE=1 ./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model Qwen/Qwen3.5-2B \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id qwen3-5-2b-local-bfcl-pilot-20260613 \
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
case failed. The successful-tool cases produced reasoning text and echoed tool
schemas or function metadata instead of exact Hermes tool-call objects. The
invalid-tool case recognized that `delete_customer_record` was unavailable, but
included excluded tool-like text and a conversational follow-up, so it failed
the no-extra-tool-text gate.

## Decision

Keep `Qwen/Qwen3.5-2B` blocked for strict Hermes tool-call promotion. It remains
usable as a helper/extractor research lane only if downstream code expects
natural-language reasoning rather than strict Hermes tool calls.
