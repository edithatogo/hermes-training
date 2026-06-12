# Hermes Qwen3.5 2B SFT v7 Q4_K_M llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`mkadrlik/hermes-Qwen3.5-2B-SFT-v7` was run through the strict Hermes
BFCL-style endpoint pilot using the cached SSD GGUF artifact and Homebrew
llama.cpp server.

Result: `1/3` cases passed, pass rate `0.333`.

This is the strongest Hermes-Qwen3.5 SFT result in this local strict pilot
slice so far. It produced one exact strict `<tool_call>` for the simple lookup
case, but still failed parallel tool-call formatting and called the forbidden
delete tool in the invalid-tool case.

## Artifact

- Repo: `mkadrlik/hermes-Qwen3.5-2B-SFT-v7`
- File: `hermes-2B-Q4_K_M.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--hermes-Qwen3.5-2B-SFT-v7/snapshots/346ca9082564b28828fd08c42f27f0bc50669adf/hermes-2B-Q4_K_M.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Cache size: `1.2G`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--mkadrlik--hermes-Qwen3.5-2B-SFT-v7/snapshots/346ca9082564b28828fd08c42f27f0bc50669adf/hermes-2B-Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 18087 \
  --ctx-size 4096 \
  --alias hermes-qwen35-2b-sft-v7-q4km \
  --jinja \
  -ngl 999
```

llama.cpp selected `peg-native` chat formatting. During the pilot calls it
reported roughly `97-98` generation tokens per second.

Runtime warning:

```text
n_ctx_seq (4096) < n_ctx_train (262144) -- the full capacity of the model will not be utilized
```

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model hermes-qwen35-2b-sft-v7-q4km \
  --base-url http://127.0.0.1:18087/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id hermes-qwen35-2b-sft-v7-q4km-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/hermes-qwen35-2b-sft-v7-q4km-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | pass | Emitted exactly one parseable `<tool_call>` for `lookup_customer`. |
| `bfcl-parallel-ticket-routing` | fail | Tried to emit both tool calls, but used malformed tags and JSON arrays that the strict parser could not accept. |
| `bfcl-invalid-tool` | fail | Emitted a JSON object calling the forbidden `delete_customer_record` tool. |

## Decision

- Status: `strict-endpoint-pilot-complete; repair-candidate; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Prefer this 2B lane over the 0.8B Hermes-Qwen3.5 lane for any prompt/profile
  repair experiments because it already passes the simplest strict tool-call
  case.
