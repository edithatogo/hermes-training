# Nanbeige 4.1 3B Transformers MPS FP16 Strict BFCL Pilot - 2026-06-13

## Summary

`Nanbeige/Nanbeige4.1-3B` was run through the strict Hermes BFCL-style local
pilot using the new generic Hugging Face Transformers runner on MPS with
`float16`.

Result: `0/3` cases passed, pass rate `0.000`.

This official Transformers path was more informative than the GGUF sibling. It
emitted a correct parseable simple lookup tool call, but wrapped it in
`<think>...</think>` text, which fails the strict no-extra-tool-text contract.
The invalid-tool case refused the unavailable delete function, but mentioned
the forbidden tool name and therefore failed the strict exclusion rule.

## Artifact

- Repo: `Nanbeige/Nanbeige4.1-3B`
- Files:
  - `model-00001-of-00002.safetensors`
  - `model-00002-of-00002.safetensors`
- Local cache: `/Volumes/PortableSSD/huggingface/hub/models--Nanbeige--Nanbeige4.1-3B`
- Cache size: `7.4G`
- Runtime: `transformers`, MPS, `float16`

## Runner

This slice added a reusable local Transformers runner:

`scripts/run_transformers_pilot_benchmark.py`

It mirrors the MLX local pilot runner but uses `AutoTokenizer` and
`AutoModelForCausalLM`, stores results under the SSD-backed
`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/` root, and
uses the same strict scoring logic as endpoint pilots.

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_transformers_pilot_benchmark.py \
  --model Nanbeige/Nanbeige4.1-3B \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id nanbeige41-3b-transformers-mps-fp16-strict-bfcl-pilot-20260613 \
  --device mps \
  --dtype float16 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/nanbeige41-3b-transformers-mps-fp16-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Produced the exact expected `lookup_customer` tool call, but included `<think>` reasoning text before the call. |
| `bfcl-parallel-ticket-routing` | fail | Generated only reasoning text within the 256-token cap and no parseable tool calls. |
| `bfcl-invalid-tool` | fail | Refused the unavailable delete function, but mentioned `delete_customer_record`, violating the strict exclusion rule. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- This lane is a useful prompt/profile repair candidate because the simple
  lookup call was structurally correct after removing reasoning text.
