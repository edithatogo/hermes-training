# mkadrlik Hermes Qwen3.5 4B SFT v7 Qwen No-Think Prefill Repair

- Candidate: `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`
- Variant: `qwen-no-think-prefill`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-4B-SFT-v7/snapshots/cab9668c98ff07d5d39f1c884e86df7b81353e02/hermes-qwen3.5-4b-Q8_0.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-4b-sft-v7-qwen-no-think-prefill-20260614-030604`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-4b-sft-v7-qwen-no-think-prefill-20260614-030604/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 0 | 0.000 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: included visible `<think>` tags and malformed
  the closing tag as `</tools>`.
- `bfcl-parallel-ticket-routing`: included visible `<think>` tags and produced
  only a partial first tool call.
- `bfcl-invalid-tool`: emitted both `lookup_customer` and forbidden
  `delete_customer_record` JSON payloads instead of refusing.

## Decision

Do not promote. The no-think/prefill variant regressed to `0/3`, so the best
4B prompt-only endpoint result remains the strict-suffix `1/3` run.
