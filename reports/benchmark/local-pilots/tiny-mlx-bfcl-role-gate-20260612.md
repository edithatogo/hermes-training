# Tiny MLX BFCL-Style Role Gate

Date: 2026-06-12
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation
Cases: 3

## Results

| Model | Cache footprint | Run ID | Passed | Pass rate | Notes |
|---|---:|---|---:|---:|---|
| `openbmb/MiniCPM5-1B-MLX` | 592M | `minicpm5-1b-mlx-local-bfcl-pilot-20260612` | 0 / 3 | 0.000 | Reasoned about tools; did not emit strict JSON tool calls; invalid-tool case attempted forbidden deletion. |
| `Qwen/Qwen3.5-0.8B` | 1.7G | `qwen35-08b-local-bfcl-pilot-20260612` | 0 / 3 | 0.000 | Reasoned about tools and refused invalid tool semantically, but emitted extra text/non-strict tags. |
| `Qwen/Qwen3.5-2B` | 4.3G | `qwen35-2b-local-bfcl-pilot-20260612` | 0 / 3 | 0.000 | Similar to 0.8B with better refusal prose, but still not strict schema-compliant. |

Raw outputs:

- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/minicpm5-1b-mlx-local-bfcl-pilot-20260612`
- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen35-08b-local-bfcl-pilot-20260612`
- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen35-2b-local-bfcl-pilot-20260612`

## Decision

None of these tiny/base MLX models is ready as a strict Hermes tool-call model
without prompt-format repair or fine-tuning. MiniCPM5 is the smallest runtime
candidate and remains useful for helper/extraction experiments. Qwen3.5 0.8B
and 2B show stronger invalid-tool refusal intent, but the strict schema still
fails.

Next useful slice:

- run a controlled assistant-prefill prompt-format retry on the same 3-case
  suite;
- if pass rate remains low, keep these models as helper/extraction candidates
  and do not spend fine-tune budget until the training objective is explicit.
