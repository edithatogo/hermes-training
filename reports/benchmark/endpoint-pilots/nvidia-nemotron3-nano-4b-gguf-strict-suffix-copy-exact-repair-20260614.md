# NVIDIA Nemotron 3 Nano 4B GGUF Strict-Suffix Endpoint Repair

- Candidate: `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--nvidia--NVIDIA-Nemotron-3-Nano-4B-GGUF/snapshots/ba223d14e45525f7fae81db77ea8cabeb2fc6c25/NVIDIA-Nemotron3-Nano-4B-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/nvidia-nvidia-nemotron-3-nano-4b-gguf-strict-suffix-copy-exact-20260614-032238`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/nvidia-nvidia-nemotron-3-nano-4b-gguf-strict-suffix-copy-exact-20260614-032238/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 1 | 0.333 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: returned empty output.
- `bfcl-parallel-ticket-routing`: emitted exact JSON payloads, but inside DSML
  `<｜DSML｜tool>` tags rather than strict Hermes `<tool_call>` blocks.
- `bfcl-invalid-tool`: passed the strict unavailable-tool refusal.

## Decision

Do not promote. The endpoint can refuse unavailable tools, but available-tool
calls are not emitted in strict Hermes format.
