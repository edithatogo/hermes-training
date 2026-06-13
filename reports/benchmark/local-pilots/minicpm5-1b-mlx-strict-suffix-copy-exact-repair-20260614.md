# MiniCPM5 1B MLX Strict-Suffix Prompt Repair

Run ID: `openbmb-minicpm5-1b-mlx-strict-suffix-copy-exact-20260614-020101`
Created: `2026-06-13T16:01:09.848329+00:00`
Model: `openbmb/MiniCPM5-1B-MLX`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, strict suffix plus exact-copy instruction
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/openbmb-minicpm5-1b-mlx-strict-suffix-copy-exact-20260614-020101`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The model emitted thinking traces, prose, markdown JSON fragments, and repeated
refusal text instead of exact Hermes tool-call blocks. The invalid-tool case
failed because the response mentioned excluded unavailable tool text.

## Decision

Do not promote `openbmb/MiniCPM5-1B-MLX` from this strict-suffix repair.
