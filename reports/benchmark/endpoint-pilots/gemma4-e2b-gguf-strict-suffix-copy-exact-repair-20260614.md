# Gemma 4 E2B GGUF Strict-Suffix Endpoint Repair

- Candidate: `google/gemma-4-E2B-it-qat-q4_0-gguf`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--google--gemma-4-E2B-it-qat-q4_0-gguf/snapshots/1894d1fc0a19d86697abd40483f5983c867df03f/gemma-4-E2B_q4_0-it.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/google-gemma-4-e2b-it-qat-q4-0-gguf-strict-suffix-copy-exact-20260614-023301`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/google-gemma-4-e2b-it-qat-q4-0-gguf-strict-suffix-copy-exact-20260614-023301/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 1 | 0.333 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: emitted a `function`/`parameters` payload inside `<tool_call>` instead of the required Hermes `name`/`arguments` payload.
- `bfcl-parallel-ticket-routing`: emitted function-like text inside `<tool_call>` blocks, not JSON tool-call objects.
- `bfcl-invalid-tool`: passed the exact unavailable-tool refusal.

## Decision

Do not promote. The strict suffix improved the refusal boundary only; it did not
produce valid raw Hermes tool calls for actionable tool cases.
