# MiniCPM5 1B MLX BFCL-Style Local Pilot

Run ID: `minicpm5-1b-mlx-local-bfcl-pilot-20260612`
Created: 2026-06-11T16:09:44.684369+00:00
Model: `openbmb/MiniCPM5-1B-MLX`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/minicpm5-1b-mlx-local-bfcl-pilot-20260612`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Category Breakdown

| Category | Cases | Pass rate |
|---|---:|---:|
| `contains_excludes` | 1 | 0.000 |
| `tool_call_exact` | 2 | 0.000 |

## Failure Pattern

MiniCPM5 1B MLX reasoned about the intended tool calls, but did not emit the
strict Hermes tool-call JSON schema. Example output for the simple lookup case:

```text
The user wants to look up a customer by ID "CUST-1007"...
</think>

[{"customer_id":"CUST-1007"}]
```

The invalid-tool refusal case also started to call the forbidden deletion tool,
so it failed the exclusion requirement.

## Decision

This keeps MiniCPM5 as a tiny runtime/load candidate only. It should not be used
as a strict Hermes tool-call model without prompt repair, assistant prefill, or
fine-tuning. The next fair comparison is a prompt-format retry against the same
3-case BFCL pilot, alongside Qwen3.5 0.8B and 2B under the same harness.
