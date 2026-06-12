# Gemma 4 E2B QAT q4_0 llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`google/gemma-4-E2B-it-qat-q4_0-gguf` was run through the strict Hermes
BFCL-style endpoint pilot using the cached SSD GGUF artifact and Homebrew
llama.cpp server.

Result: `1/3` cases passed, pass rate `0.333`.

This is useful runtime-adapter evidence, but not a promotion result. The model
loaded and answered quickly, but emitted Gemma/native or malformed tool-call
payload shapes instead of the strict Hermes `<tool_call>{"name":...,
"arguments":...}</tool_call>` schema.

## Artifact

- Repo: `google/gemma-4-E2B-it-qat-q4_0-gguf`
- File: `gemma-4-E2B_q4_0-it.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--google--gemma-4-E2B-it-qat-q4_0-gguf/snapshots/1894d1fc0a19d86697abd40483f5983c867df03f/gemma-4-E2B_q4_0-it.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--google--gemma-4-E2B-it-qat-q4_0-gguf/snapshots/1894d1fc0a19d86697abd40483f5983c867df03f/gemma-4-E2B_q4_0-it.gguf \
  --host 127.0.0.1 \
  --port 18082 \
  --ctx-size 4096 \
  --alias google-gemma-4-e2b-it-qat-q4-0-gguf \
  --jinja \
  -ngl 999
```

llama.cpp selected the `peg-gemma4` chat format and reported about `97-100`
generation tokens per second during the three short pilot calls. Startup kept
the same warnings seen in the earlier smoke: control-looking `<|tool_response>`
and `</s>` token metadata were overridden, and `</s>` was removed from the EOG
list.

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model google-gemma-4-e2b-it-qat-q4-0-gguf \
  --base-url http://127.0.0.1:18082/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id gemma4-e2b-q4-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/gemma4-e2b-q4-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Emitted `{"function":{"name":...,"parameters":...}}`, which is not the Hermes strict schema. |
| `bfcl-parallel-ticket-routing` | fail | Emitted `create_ticket{...}` and `assign_ticket{...}` inside tool tags, which is not parseable JSON. |
| `bfcl-invalid-tool` | pass | Refused the unavailable delete operation without emitting a forbidden tool call. |

## Decision

- Status: `strict-endpoint-pilot-complete; prompt-profile-repair-needed`
- Do not promote to Hermes default, training, or publication.
- Keep as an adapter-repair candidate because the runtime is fast and the
  invalid-tool refusal passed, but strict tool-call emission is not yet usable.
