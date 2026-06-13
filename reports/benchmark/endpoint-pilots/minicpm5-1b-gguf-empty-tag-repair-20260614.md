# MiniCPM5 1B GGUF Empty-Tag Endpoint Repair

- Candidate: `openbmb/MiniCPM5-1B-GGUF`
- Variant: `minicpm-empty-tag-repair`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--openbmb--MiniCPM5-1B-GGUF/snapshots/87007042419d30c1d8f38ef065424ee33870831e/MiniCPM5-1B-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/openbmb-minicpm5-1b-gguf-minicpm-empty-tag-repair-20260614-032828`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/openbmb-minicpm5-1b-gguf-minicpm-empty-tag-repair-20260614-032828/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 1 | 0.333 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: emitted a tag-like fragment with the right
  function name and customer id, but no strict Hermes `<tool_call>` block.
- `bfcl-parallel-ticket-routing`: refused an available routing request instead
  of emitting the listed parallel tool calls.
- `bfcl-invalid-tool`: passed the strict unavailable-tool refusal.

## Decision

Do not promote. The best MiniCPM5 GGUF endpoint repair only passed unavailable
tool refusal and still failed exact tool-call parsing.
