# LFM2.5 8B A1B GGUF Strict-Suffix Endpoint Repair

- Candidate: `LiquidAI/LFM2.5-8B-A1B-GGUF`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--LiquidAI--LFM2.5-8B-A1B-GGUF/snapshots/dfd5fdcad7a1c0d31473fb4ca443b8befbacddf0/LFM2.5-8B-A1B-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/liquidai-lfm2-5-8b-a1b-gguf-strict-suffix-copy-exact-20260614-024103`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/liquidai-lfm2-5-8b-a1b-gguf-strict-suffix-copy-exact-20260614-024103/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 0 | 0.000 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: refused database access instead of emitting the available `lookup_customer` tool call.
- `bfcl-parallel-ticket-routing`: refused unavailable tools despite `create_ticket` and `assign_ticket` being listed.
- `bfcl-invalid-tool`: mentioned the forbidden `delete_customer_record` tool and offered an alternate lookup, failing the strict refusal boundary.

## Decision

Do not promote. The strict suffix did not produce valid raw Hermes tool calls or
a clean unavailable-tool refusal for this endpoint run.
