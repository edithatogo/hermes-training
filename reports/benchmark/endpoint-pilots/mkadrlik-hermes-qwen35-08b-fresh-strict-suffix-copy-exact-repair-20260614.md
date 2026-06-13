# mkadrlik Hermes Qwen3.5 0.8B Fresh Strict-Suffix Endpoint Repair

- Candidate: `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--hermes-Qwen3.5-0.8B-SFT-v7-fresh/snapshots/954dc26fe3d5167bd93c49b63719ac06b5b62093/hermes-0.8B-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh-strict-suffix-copy-exact-20260614-031653`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh-strict-suffix-copy-exact-20260614-031653/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 0 | 0.000 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: emitted JSON between wrapper glyphs instead
  of a strict Hermes `<tool_call>` block.
- `bfcl-parallel-ticket-routing`: altered the ticket title and used malformed
  `</tool>` / `</template>` tags.
- `bfcl-invalid-tool`: emitted an `execute_code` payload rather than refusing.

## Decision

Do not promote. The strict profile produced no valid strict cases.
