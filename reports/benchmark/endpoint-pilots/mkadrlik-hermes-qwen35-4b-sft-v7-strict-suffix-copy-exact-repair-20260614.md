# mkadrlik Hermes Qwen3.5 4B SFT v7 Strict-Suffix Endpoint Repair

- Candidate: `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-4B-SFT-v7/snapshots/cab9668c98ff07d5d39f1c884e86df7b81353e02/hermes-qwen3.5-4b-Q8_0.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-4b-sft-v7-strict-suffix-copy-exact-20260614-030449`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-4b-sft-v7-strict-suffix-copy-exact-20260614-030449/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 1 | 0.333 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: passed with a valid exact Hermes
  `lookup_customer` tool call.
- `bfcl-parallel-ticket-routing`: emitted two correct-looking JSON payloads but
  malformed the Hermes envelope, using a second `<tool_call>` opener and
  `</tools>` closing tag.
- `bfcl-invalid-tool`: refused the unavailable operation but mentioned the
  forbidden `delete_customer_record` tool name.

## Decision

Do not promote. The strict suffix proves simple-call viability, but malformed
parallel envelopes and forbidden-tool leakage block raw Hermes promotion.
