# ManiacLabs Qwen3.6 35B A3B 2bit Qwen No-Think Prefill Repair

- Candidate: `ManiacLabs/Qwen3.6-35B-A3B-2bit`
- Variant: `qwen-no-think-prefill`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--ManiacLabs--Qwen3.6-35B-A3B-2bit/snapshots/5f92fade67bd6712b339fad950f86296d1b0a71e/qwen3.6-35b-a3b-iq2xxs-q2k.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/maniaclabs-qwen3-6-35b-a3b-2bit-qwen-no-think-prefill-20260614-025622`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/maniaclabs-qwen3-6-35b-a3b-2bit-qwen-no-think-prefill-20260614-025622/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 1 | 0.333 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: included visible `<think>` tags and emitted a
  non-JSON `lookup_customer` payload inside the tool block.
- `bfcl-parallel-ticket-routing`: included visible `<think>` tags and a
  non-Hermes `<tools>` structure instead of exact tool-call blocks.
- `bfcl-invalid-tool`: passed the strict unavailable-tool refusal text match,
  but still included the visible prefill prefix in raw output.

## Decision

Do not promote. The no-think/prefill path regressed to `1/3` and introduces
visible hidden-reasoning tags, so the best ManiacLabs prompt-only result remains
the `empty-output-retry` `2/3` endpoint run.
