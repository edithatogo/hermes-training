# Qwen3.5 2B No-Think Prefill Repair

Run ID: `qwen-qwen3-5-2b-qwen-no-think-prefill-20260614-020640`
Created: `2026-06-13T16:07:00.772771+00:00`
Model: `Qwen/Qwen3.5-2B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, `/no_think` user prefix, empty `<think>` assistant prefill
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen-qwen3-5-2b-qwen-no-think-prefill-20260614-020640`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 1 |
| Pass rate | 0.333 |

## Failure Pattern

No-think prefill fixed the invalid-tool refusal but still failed both exact
tool-call cases by emitting repeated malformed `<tool_call>` fragments that did
not parse as exact Hermes calls.

## Decision

Do not promote `Qwen/Qwen3.5-2B` from this repair. All queued prompt-only local
variants have failed strict promotion; use a grammar/envelope-constrained path
or move to the next local candidate.
