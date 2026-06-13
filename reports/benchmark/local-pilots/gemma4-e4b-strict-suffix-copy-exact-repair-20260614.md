# Gemma E4B Strict-Suffix Prompt Repair

Run ID: `mlx-community-gemma-4-e4b-it-qat-4bit-strict-suffix-copy-exact-20260614-020948`
Created: `2026-06-13T16:10:13.959642+00:00`
Model: `mlx-community/gemma-4-E4B-it-qat-4bit`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, strict suffix plus exact-copy instruction
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/mlx-community-gemma-4-e4b-it-qat-4bit-strict-suffix-copy-exact-20260614-020948`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The model produced Gemma-style thought channel text and native-looking
`function`/`args` or `function`/`parameters` payloads. These did not satisfy the
strict Hermes `name`/`arguments` parser, and the invalid-tool case mentioned the
excluded unavailable tool name in the thought trace.

## Decision

Do not promote `mlx-community/gemma-4-E4B-it-qat-4bit` from this raw strict
repair.
