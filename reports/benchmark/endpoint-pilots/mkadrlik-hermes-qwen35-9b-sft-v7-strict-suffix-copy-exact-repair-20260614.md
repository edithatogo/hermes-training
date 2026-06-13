# mkadrlik Hermes Qwen3.5 9B SFT v7 Strict-Suffix Endpoint Repair

- Candidate: `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-9B-SFT-v7/snapshots/bd668b3cfd376d0b961ef43736b5b58ec7978fc0/hermes-qwen3.5-9b-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-9b-sft-v7-strict-suffix-copy-exact-20260614-030954`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-9b-sft-v7-strict-suffix-copy-exact-20260614-030954/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 1 | 0.333 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: emitted `parameters` instead of required
  `arguments`, so strict Hermes parsing failed.
- `bfcl-parallel-ticket-routing`: emitted `parameters` and malformed the
  parallel envelope.
- `bfcl-invalid-tool`: passed the strict unavailable-tool refusal.

## Decision

Do not promote. The strict suffix fixed refusal wording for this endpoint, but
tool-call payload keys and parallel envelopes remain incompatible with strict
Hermes scoring.
