# ManiacLabs Qwen3.6 35B A3B 2bit Empty-Output Retry Repair

- Candidate: `ManiacLabs/Qwen3.6-35B-A3B-2bit`
- Variant: `empty-output-retry`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--ManiacLabs--Qwen3.6-35B-A3B-2bit/snapshots/5f92fade67bd6712b339fad950f86296d1b0a71e/qwen3.6-35b-a3b-iq2xxs-q2k.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/maniaclabs-qwen3-6-35b-a3b-2bit-empty-output-retry-20260614-025351`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/maniaclabs-qwen3-6-35b-a3b-2bit-empty-output-retry-20260614-025351/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 2 | 0.667 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: emitted the correct tool name and argument
  value, but used `<tool_call>...<tool_call>` instead of a closed
  `</tool_call>` block, so strict parsing failed.
- `bfcl-parallel-ticket-routing`: passed with exact `create_ticket` and
  `assign_ticket` calls.
- `bfcl-invalid-tool`: passed the strict unavailable-tool refusal.

## Decision

Do not promote. The retry instruction improved the endpoint from `1/3` to
`2/3`, but the remaining malformed single-call envelope blocks raw Hermes
promotion and requires either a no-think/prefill variant, constrained decoding,
or a runtime wrapper plus held-out proof.
