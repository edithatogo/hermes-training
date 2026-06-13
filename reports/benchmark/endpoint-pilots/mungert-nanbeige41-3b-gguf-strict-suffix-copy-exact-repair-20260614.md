# Mungert Nanbeige4.1 3B GGUF Strict-Suffix Endpoint Repair

- Candidate: `Mungert/Nanbeige4.1-3B-GGUF`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--Mungert--Nanbeige4.1-3B-GGUF/snapshots/7a35d8054f29ebe6fecc7e54b2b2e313e4307e63/Nanbeige4.1-3B-q4_k_m.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mungert-nanbeige4-1-3b-gguf-strict-suffix-copy-exact-20260614-025949`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mungert-nanbeige4-1-3b-gguf-strict-suffix-copy-exact-20260614-025949/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 1 | 0.333 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: passed with a valid exact Hermes
  `lookup_customer` tool call.
- `bfcl-parallel-ticket-routing`: returned empty output instead of the required
  parallel tool calls.
- `bfcl-invalid-tool`: refused the unavailable operation but mentioned the
  forbidden `delete_customer_record` tool name, failing the strict exclusion.

## Decision

Do not promote. The strict suffix proves the endpoint can produce one exact
Hermes call, but it still fails parallel-call emission and strict unavailable
tool refusal.
