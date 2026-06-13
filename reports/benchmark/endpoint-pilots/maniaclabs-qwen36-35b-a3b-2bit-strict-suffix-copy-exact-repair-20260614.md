# ManiacLabs Qwen3.6 35B A3B 2bit Strict-Suffix Endpoint Repair

- Candidate: `ManiacLabs/Qwen3.6-35B-A3B-2bit`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--ManiacLabs--Qwen3.6-35B-A3B-2bit/snapshots/5f92fade67bd6712b339fad950f86296d1b0a71e/qwen3.6-35b-a3b-iq2xxs-q2k.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/maniaclabs-qwen3-6-35b-a3b-2bit-strict-suffix-copy-exact-20260614-024948`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/maniaclabs-qwen3-6-35b-a3b-2bit-strict-suffix-copy-exact-20260614-024948/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 1 | 0.333 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: emitted an unclosed/malformed
  `<tool_call>` block, leaving all output as non-strict leftover text.
- `bfcl-parallel-ticket-routing`: returned an empty response instead of the
  required `create_ticket` and `assign_ticket` tool calls.
- `bfcl-invalid-tool`: passed the strict unavailable-tool refusal.

## Decision

Do not promote. The strict suffix repaired the unavailable-tool refusal only,
while both available-tool cases still failed raw Hermes tool-call formatting.
