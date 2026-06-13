# MiniCPM5 1B GGUF Strict-Suffix Endpoint Repair

- Candidate: `openbmb/MiniCPM5-1B-GGUF`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Runtime: `llama-server` with Metal offload
- Artifact: `/Volumes/PortableSSD/huggingface/hub/models--openbmb--MiniCPM5-1B-GGUF/snapshots/87007042419d30c1d8f38ef065424ee33870831e/MiniCPM5-1B-Q4_K_M.gguf`
- Source output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/openbmb-minicpm5-1b-gguf-strict-suffix-copy-exact-20260614-032828`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/openbmb-minicpm5-1b-gguf-strict-suffix-copy-exact-20260614-032828/summary.json`

## Result

| Suite | Cases | Passed | Pass rate |
|---|---:|---:|---:|
| `benchmarks/endpoint_pilots/bfcl_pilot.json` | 3 | 0 | 0.000 |

## Failure Pattern

- `bfcl-simple-customer-lookup`: refused an available lookup tool and repeated
  the refusal with extra text.
- `bfcl-parallel-ticket-routing`: asked for a team name instead of emitting the
  listed tool calls.
- `bfcl-invalid-tool`: included the forbidden unavailable tool name and extra
  explanatory text, failing the strict exclusion.

## Decision

Do not promote. The strict suffix did not produce any valid Hermes tool-call or
strict refusal cases.
