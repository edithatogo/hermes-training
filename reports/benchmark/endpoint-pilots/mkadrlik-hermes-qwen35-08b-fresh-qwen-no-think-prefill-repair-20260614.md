# mkadrlik Hermes Qwen3.5 0.8B Fresh Qwen No-Think Prefill Repair

- Candidate: `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`
- Variant: `qwen-no-think-prefill`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--hermes-Qwen3.5-0.8B-SFT-v7-fresh/snapshots/954dc26fe3d5167bd93c49b63719ac06b5b62093/hermes-0.8B-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh-qwen-no-think-prefill-20260614-031659`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh-qwen-no-think-prefill-20260614-031659/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 0 | 0.000 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: responded with visible `<think>` tags and
  prose instead of a tool call.
- `bfcl-parallel-ticket-routing`: responded with visible `<think>` tags and
  prose ticket details instead of tool calls.
- `bfcl-invalid-tool`: mentioned `delete_customer_record` and suggested an
  alternate workflow, failing strict refusal.

## Decision

Do not promote. No-think/prefill also scored `0/3`.
