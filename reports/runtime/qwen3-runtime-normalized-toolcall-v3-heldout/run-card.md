# Runtime Card: Qwen3 V3 Runtime-Normalized Tool Calls

Date: 2026-05-24

## Scope

This card records Hermes integration recoverability for the Qwen3 4B strict tool-call V3 adapter. It does not change the strict benchmark publication gate.

## Source

- Strict benchmark run: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v3-nothink-heldout-20260522/results.jsonl`
- Runtime-normalized report: `/Volumes/PortableSSD/hermes-evals/runtime-normalized-tool-call/qwen3-4b-strict-toolcall-v3-heldout-20260524/summary.md`
- Reporting script: `scripts/summarize_runtime_normalized_tool_calls.py`

## Result

| Metric | Score |
|---|---:|
| Held-out strict pass | 0.250 |
| Runtime-normalized pass | 0.875 |
| Responses with leading empty-think wrapper | 8 / 8 |
| Strict failures rescued by runtime normalization | 5 |
| Residual runtime failures | 1 |

Residual failure:

- `heldout-argument-correctness-lab-order`

## Decision

Runtime normalization is useful for local Hermes integration because it recovers otherwise correct tool calls that are blocked only by an empty leading Qwen `<think></think>` wrapper. It is not publication evidence. Hugging Face adapter publication remains blocked until the strict held-out pass rate reaches `1.000`.
