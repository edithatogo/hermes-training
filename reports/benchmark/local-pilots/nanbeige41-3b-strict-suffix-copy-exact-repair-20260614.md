# Nanbeige 4.1 3B Strict-Suffix Prompt Repair

Run ID: `nanbeige-nanbeige4-1-3b-strict-suffix-copy-exact-20260614-021619`
Created: `2026-06-13T16:16:56.796542+00:00`
Model: `Nanbeige/Nanbeige4.1-3B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local Transformers/MLX-compatible generation, SSD cache, strict suffix plus exact-copy instruction
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/nanbeige-nanbeige4-1-3b-strict-suffix-copy-exact-20260614-021619`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The two tool-call cases produced correct Hermes `name` and `arguments` payloads,
but they failed strict scoring because `<think>` traces remained before the
calls. The invalid-tool case also included extra explanation and mentioned the
unavailable delete tool after the required refusal.

## Decision

Do not promote `Nanbeige/Nanbeige4.1-3B` from this repair. The remaining blocker
is strict no-extra-text formatting; a future revisit should use no-think or a
grammar/envelope-constrained output path.
