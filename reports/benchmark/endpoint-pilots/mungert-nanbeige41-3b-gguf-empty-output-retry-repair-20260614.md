# Mungert Nanbeige4.1 3B GGUF Empty-Output Retry Repair

- Candidate: `Mungert/Nanbeige4.1-3B-GGUF`
- Variant: `empty-output-retry`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--Mungert--Nanbeige4.1-3B-GGUF/snapshots/7a35d8054f29ebe6fecc7e54b2b2e313e4307e63/Nanbeige4.1-3B-q4_k_m.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mungert-nanbeige4-1-3b-gguf-empty-output-retry-20260614-030035`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mungert-nanbeige4-1-3b-gguf-empty-output-retry-20260614-030035/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 1 | 0.333 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: passed with a valid exact Hermes
  `lookup_customer` tool call.
- `bfcl-parallel-ticket-routing`: still returned empty output despite the
  direct non-empty tool-call instruction.
- `bfcl-invalid-tool`: refused the unavailable operation but named
  `delete_customer_record` and offered an alternate lookup, failing the strict
  refusal boundary.

## Decision

Do not promote. The retry variant did not improve over strict suffix, so
Mungert Nanbeige4.1 3B GGUF remains blocked by empty parallel-call output and
forbidden-tool leakage.
