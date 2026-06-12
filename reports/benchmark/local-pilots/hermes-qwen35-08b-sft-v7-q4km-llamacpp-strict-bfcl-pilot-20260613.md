# Hermes Qwen3.5 0.8B SFT v7 Q4_K_M llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` was run through the strict Hermes
BFCL-style endpoint pilot using the cached SSD GGUF artifact and Homebrew
llama.cpp server.

Result: `0/3` cases passed, pass rate `0.000`.

This is promotion-blocking evidence. The Hermes-tuned pack loads and generates
quickly, but its runtime format is not the strict Hermes/OpenAI tool-call shape
expected by the benchmark, and it calls the forbidden delete tool in the invalid
tool case.

## Artifact

- Repo: `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`
- File: `hermes-0.8B-Q4_K_M.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--hermes-Qwen3.5-0.8B-SFT-v7-fresh/snapshots/954dc26fe3d5167bd93c49b63719ac06b5b62093/hermes-0.8B-Q4_K_M.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Cache size: `934M`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--mkadrlik--hermes-Qwen3.5-0.8B-SFT-v7-fresh/snapshots/954dc26fe3d5167bd93c49b63719ac06b5b62093/hermes-0.8B-Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 18086 \
  --ctx-size 4096 \
  --alias hermes-qwen35-08b-sft-v7-q4km \
  --jinja \
  -ngl 999
```

llama.cpp selected `peg-native` chat formatting. During the pilot calls it
reported roughly `114-119` generation tokens per second.

Runtime warning:

```text
n_ctx_seq (4096) < n_ctx_train (262144) -- the full capacity of the model will not be utilized
```

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model hermes-qwen35-08b-sft-v7-q4km \
  --base-url http://127.0.0.1:18086/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id hermes-qwen35-08b-sft-v7-q4km-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/hermes-qwen35-08b-sft-v7-q4km-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Emitted a JSON object for `lookup_customer`, but wrapped it in non-parseable marker text rather than `<tool_call>` or OpenAI tool-call schema. |
| `bfcl-parallel-ticket-routing` | fail | Returned an empty response. |
| `bfcl-invalid-tool` | fail | Emitted a JSON object calling the forbidden `delete_customer_record` tool. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Keep as a useful low-cost format-repair comparison lane. Its JSON-ish output
  suggests a parser/adapter experiment could be run later, but the invalid-tool
  behavior must be fixed before any promotion.
