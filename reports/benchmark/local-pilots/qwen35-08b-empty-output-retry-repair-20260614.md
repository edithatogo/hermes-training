# Qwen3.5 0.8B Empty-Output Retry Repair

Run ID: `qwen-qwen3-5-0-8b-empty-output-retry-20260614-015854`
Created: `2026-06-13T15:59:05.258377+00:00`
Model: `Qwen/Qwen3.5-0.8B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, empty-output retry suffix, strict no-extra-tool-text scoring
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen-qwen3-5-0-8b-empty-output-retry-20260614-015854`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The variant did not repair strict tool-call behavior:

| Case | Category | Result |
|---|---|---|
| `bfcl-simple-customer-lookup` | `tool_call_exact` | Failed; emitted reasoning text plus a tool schema fragment rather than copied call arguments. |
| `bfcl-parallel-ticket-routing` | `tool_call_exact` | Failed; emitted a long thinking trace and no parseable Hermes tool calls. |
| `bfcl-invalid-tool` | `contains_excludes` | Failed; included reasoning and unavailable tool text around the refusal. |

## Decision

Do not promote `Qwen/Qwen3.5-0.8B` from this repair. All queued local prompt-only
repair variants for this candidate have now failed the strict BFCL pilot. The
remaining useful work is either a grammar/envelope-constrained runtime path or
moving local repair effort to the next queued candidate.
