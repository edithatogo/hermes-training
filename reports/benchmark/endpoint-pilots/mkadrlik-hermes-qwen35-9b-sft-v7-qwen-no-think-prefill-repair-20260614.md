# mkadrlik Hermes Qwen3.5 9B SFT v7 Qwen No-Think Prefill Repair

- Candidate: `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`
- Variant: `qwen-no-think-prefill`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-9B-SFT-v7/snapshots/bd668b3cfd376d0b961ef43736b5b58ec7978fc0/hermes-qwen3.5-9b-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-9b-sft-v7-qwen-no-think-prefill-20260614-031117`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-9b-sft-v7-qwen-no-think-prefill-20260614-031117/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 0 | 0.000 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: emitted the exact lookup call, but visible
  `<think>` text violated no-extra-text scoring.
- `bfcl-parallel-ticket-routing`: emitted only the first required tool call and
  retained visible `<think>` text.
- `bfcl-invalid-tool`: emitted a lookup payload instead of the required refusal.

## Decision

Do not promote. The no-think/prefill variant regressed to `0/3`, so the best
9B prompt-only endpoint result remains the strict-suffix `1/3` run.
