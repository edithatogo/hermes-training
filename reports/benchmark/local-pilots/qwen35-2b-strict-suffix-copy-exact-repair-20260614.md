# Qwen3.5 2B Strict-Suffix Prompt Repair

Run ID: `qwen-qwen3-5-2b-strict-suffix-copy-exact-20260614-020549`
Created: `2026-06-13T16:06:06.333428+00:00`
Model: `Qwen/Qwen3.5-2B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, strict suffix plus exact-copy instruction
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen-qwen3-5-2b-strict-suffix-copy-exact-20260614-020549`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The model emitted thinking text and malformed schema-like tool fragments. The
invalid-tool refusal included unavailable tool text, so the strict excludes gate
failed.

## Decision

Do not promote `Qwen/Qwen3.5-2B` from this strict-suffix repair.
