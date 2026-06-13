# Granite 4.1 3B Strict-Suffix Prompt Repair

Run ID: `ibm-granite-granite-4-1-3b-strict-suffix-copy-exact-20260614-021324`
Created: `2026-06-13T16:13:38.961511+00:00`
Model: `ibm-granite/granite-4.1-3b`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, strict suffix plus exact-copy instruction
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/ibm-granite-granite-4-1-3b-strict-suffix-copy-exact-20260614-021324`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 1 |
| Pass rate | 0.333 |

## Failure Pattern

The model passed only the invalid-tool refusal case. The customer lookup emitted
a native function array plus trailing `<tool_call>` text, and the ticket case
emitted only argument JSON rather than exact Hermes tool-call blocks.

## Decision

Do not promote `ibm-granite/granite-4.1-3b` from this raw strict repair.
