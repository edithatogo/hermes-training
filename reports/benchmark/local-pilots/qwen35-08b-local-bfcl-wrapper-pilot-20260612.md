# Qwen3.5 0.8B BFCL Wrapper Pilot

Run ID: `qwen35-08b-local-bfcl-wrapper-pilot-20260612`
Created: 2026-06-11T16:17:55.590084+00:00
Model: `Qwen/Qwen3.5-0.8B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation with assistant prefill and score wrapper
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen35-08b-local-bfcl-wrapper-pilot-20260612`

## Prompt/Scoring Profile

```text
assistant_prefill = <tool_call>
score_prefix = <tool_call>
score_suffix = </tool_call>
max_tokens = 96
```

The raw generated response is preserved in `response`; `scored_response` records
the explicit wrapper used only for scoring.

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The wrapper did not repair strict tool-call behavior. It pushed the model toward
repeating tool metadata and function-style fragments rather than emitting the
expected Hermes JSON tool-call objects. The invalid-tool case still produced a
tool-like call to `lookup_customer`, so it failed refusal/exclusion.

## Decision

Simple assistant-prefill wrapping is not enough for Qwen3.5 0.8B on this pilot.
Do not promote it for strict Hermes tool calling. The next step is either a
different prompt profile that suppresses `<tools>` echoing, or a small targeted
fine-tune objective.
