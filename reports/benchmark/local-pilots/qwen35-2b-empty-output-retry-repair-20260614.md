# Qwen3.5 2B Empty-Output Retry Repair

Run ID: `qwen-qwen3-5-2b-empty-output-retry-20260614-020612`
Created: `2026-06-13T16:06:34.797502+00:00`
Model: `Qwen/Qwen3.5-2B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, empty-output retry suffix
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen-qwen3-5-2b-empty-output-retry-20260614-020612`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The retry suffix caused repeated malformed tool-call fragments and still
included unavailable tool text in the invalid-tool refusal path.

## Decision

Do not promote `Qwen/Qwen3.5-2B` from this empty-output retry repair.
