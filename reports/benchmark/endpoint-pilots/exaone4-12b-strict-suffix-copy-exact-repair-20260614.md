# EXAONE 4.0 1.2B Strict-Suffix Endpoint Repair

- Candidate: `LGAI-EXAONE/EXAONE-4.0-1.2B`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--LGAI-EXAONE--EXAONE-4.0-1.2B-GGUF/snapshots/162446400ea4596377a3ce1d3ddffa32971af0a6/EXAONE-4.0-1.2B-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/lgai-exaone-exaone-4-0-1-2b-strict-suffix-copy-exact-20260614-022518`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/lgai-exaone-exaone-4-0-1-2b-strict-suffix-copy-exact-20260614-022518/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 0 | 0.000 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: refused tool access and gave CRM/database advice instead of a Hermes tool call.
- `bfcl-parallel-ticket-routing`: drafted a prose incident ticket instead of emitting the expected parallel tool calls.
- `bfcl-invalid-tool`: hallucinated `delete_customer_record` calls instead of refusing the unavailable tool.

## Decision

Do not promote. The endpoint run shows EXAONE 1.2B is not responsive to the
strict Hermes suffix for raw tool-call compliance. Revisit only through a
different prompt family, constrained output, or a non-raw normalizing envelope.
