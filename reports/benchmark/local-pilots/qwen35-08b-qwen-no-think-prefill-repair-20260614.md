# Qwen3.5 0.8B No-Think Prefill Repair

Run ID: `qwen-qwen3-5-0-8b-qwen-no-think-prefill-20260614-015642`
Created: `2026-06-13T15:56:50.420690+00:00`
Model: `Qwen/Qwen3.5-0.8B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, `/no_think` user prefix, empty `<think>` assistant prefill, strict no-extra-tool-text scoring
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen-qwen3-5-0-8b-qwen-no-think-prefill-20260614-015642`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 1 |
| Pass rate | 0.333 |

## Failure Pattern

The variant improved over strict suffix only by producing the exact refusal for
the invalid-tool case. It still failed both exact tool-call cases:

| Case | Category | Result |
|---|---|---|
| `bfcl-simple-customer-lookup` | `tool_call_exact` | Failed; emitted a tool schema fragment instead of a Hermes call with copied `customer_id`. |
| `bfcl-parallel-ticket-routing` | `tool_call_exact` | Failed; emitted non-parseable function fragments instead of exact Hermes tool-call blocks. |
| `bfcl-invalid-tool` | `contains_excludes` | Passed; emitted the exact unavailable-tool refusal without excluded tool text. |

## Decision

Do not promote `Qwen/Qwen3.5-0.8B` from this repair. The no-think controls help
refusal behavior but do not repair strict Hermes tool-call parsing. The next
local repair should test `empty-output-retry` or a grammar/envelope-constrained
generation path rather than relying on prompt suffixes alone.
