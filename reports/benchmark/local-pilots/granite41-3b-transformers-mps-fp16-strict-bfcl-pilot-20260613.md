# Granite 4.1 3B Transformers MPS FP16 Strict BFCL Pilot - 2026-06-13

## Summary

`ibm-granite/granite-4.1-3b` was run through the strict Hermes BFCL-style
local pilot using the generic Hugging Face Transformers runner on MPS with
`float16`.

Result: `1/3` cases passed, pass rate `0.333`.

The model loaded and generated quickly once the SSD-backed weights were
available, but it is not compatible with the current strict Hermes tool-call
parser without a prompt/profile adapter or output normalizer.

## Artifact

- Repo: `ibm-granite/granite-4.1-3b`
- Local cache: `/Volumes/PortableSSD/huggingface/hub/models--ibm-granite--granite-4.1-3b`
- Cache size after acquisition: `6.0G`
- Runtime: Hugging Face Transformers
- Device: MPS
- Dtype: `float16`
- Load time reported by runner: `645.6s`

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_transformers_pilot_benchmark.py \
  --model ibm-granite/granite-4.1-3b \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id granite41-3b-transformers-mps-fp16-strict-bfcl-pilot-20260613 \
  --device mps \
  --dtype float16 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/granite41-3b-transformers-mps-fp16-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Emitted a function-call-shaped JSON object, but used a wrapper/schema that produced a parse error and left extra text. |
| `bfcl-parallel-ticket-routing` | fail | Emitted only one argument object rather than the two expected Hermes tool calls. |
| `bfcl-invalid-tool` | pass | Correctly refused the unavailable delete operation without mentioning the forbidden function name. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Keep as a helper/extraction comparison lane and prompt/profile repair
  candidate.
