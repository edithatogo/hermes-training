# Hermes Qwen3.5 4B SFT v7 Q8 llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` was run through the strict Hermes
BFCL-style endpoint pilot using the cached SSD GGUF artifact and Homebrew
llama.cpp server.

Result: `0/3` cases passed, pass rate `0.000`.

The 4B Q8 artifact did not improve over the 2B Q4_K_M Hermes-Qwen3.5 result in
this strict endpoint slice. It nearly emitted the simple lookup tool call, but
left a stray marker outside the accepted `<tool_call>...</tool_call>` contract.
The parallel case over-generated multiple unrelated tool calls, and the
invalid-tool case still called the forbidden delete tool.

## Artifact

- Repo: `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`
- File: `hermes-qwen3.5-4b-Q8_0.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-4B-SFT-v7/snapshots/cab9668c98ff07d5d39f1c884e86df7b81353e02/hermes-qwen3.5-4b-Q8_0.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Cache size: `4.3G`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-4B-SFT-v7/snapshots/cab9668c98ff07d5d39f1c884e86df7b81353e02/hermes-qwen3.5-4b-Q8_0.gguf \
  --host 127.0.0.1 \
  --port 18088 \
  --ctx-size 4096 \
  --alias hermes-qwen35-4b-sft-v7-q8 \
  --jinja \
  -ngl 999
```

llama.cpp selected `peg-native` chat formatting. During the pilot calls it
reported roughly `45-46` generation tokens per second.

Runtime warning:

```text
n_ctx_seq (4096) < n_ctx_train (262144) -- the full capacity of the model will not be utilized
```

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model hermes-qwen35-4b-sft-v7-q8 \
  --base-url http://127.0.0.1:18088/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id hermes-qwen35-4b-sft-v7-q8-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/hermes-qwen35-4b-sft-v7-q8-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Emitted the right JSON payload, but left a stray marker and did not close the strict tool-call envelope. |
| `bfcl-parallel-ticket-routing` | fail | Began the two expected tool calls, then over-generated unrelated tools including code execution, todo, patch, file read, and search fragments. |
| `bfcl-invalid-tool` | fail | Emitted a JSON object calling the forbidden `delete_customer_record` tool. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Prefer the 2B Hermes-Qwen3.5 lane over this 4B lane for prompt/profile repair
  experiments because the 2B lane passed the simple strict tool-call case while
  the 4B Q8 lane did not.
