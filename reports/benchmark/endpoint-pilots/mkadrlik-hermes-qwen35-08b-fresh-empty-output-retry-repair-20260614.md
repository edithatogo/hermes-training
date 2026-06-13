# mkadrlik Hermes Qwen3.5 0.8B Fresh Empty-Output Retry Repair

- Candidate: `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`
- Variant: `empty-output-retry`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--hermes-Qwen3.5-0.8B-SFT-v7-fresh/snapshots/954dc26fe3d5167bd93c49b63719ac06b5b62093/hermes-0.8B-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh-empty-output-retry-20260614-031656`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh-empty-output-retry-20260614-031656/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 0 | 0.000 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: repeated the wrapper-glyph JSON shape.
- `bfcl-parallel-ticket-routing`: returned empty output.
- `bfcl-invalid-tool`: emitted an `execute_code` payload and mentioned
  `delete_customer_record`, failing the strict exclusion.

## Decision

Do not promote. Empty-output retry did not repair any strict case.
