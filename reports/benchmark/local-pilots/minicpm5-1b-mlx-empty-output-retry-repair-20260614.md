# MiniCPM5 1B MLX Empty-Output Retry Repair

Run ID: `openbmb-minicpm5-1b-mlx-empty-output-retry-20260614-020121`
Created: `2026-06-13T16:01:29.673740+00:00`
Model: `openbmb/MiniCPM5-1B-MLX`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, empty-output retry suffix
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/openbmb-minicpm5-1b-mlx-empty-output-retry-20260614-020121`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The retry suffix did not produce exact tool calls. The model emitted reasoning
text, treated the ticket assignment as underspecified, and failed the invalid
tool case by mentioning excluded unavailable tool text.

## Decision

Do not promote `openbmb/MiniCPM5-1B-MLX` from this empty-output retry repair.
