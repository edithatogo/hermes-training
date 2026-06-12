# Maniac Qwen3.6 35B-A3B 2-bit GGUF llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`ManiacLabs/Qwen3.6-35B-A3B-2bit` was run through the strict Hermes
BFCL-style endpoint pilot using the cached SSD GGUF artifact and Homebrew
llama.cpp server.

Result: `0/3` cases passed, pass rate `0.000`.

The model loaded successfully and generated at roughly `42-43` tokens per
second on the M1 Max. The strict Hermes tool-call behavior was not usable in
this prompt/profile slice: two cases returned empty assistant content, and the
parallel case emitted a malformed partial tool-call fragment.

## Artifact

- Repo: `ManiacLabs/Qwen3.6-35B-A3B-2bit`
- File: `qwen3.6-35b-a3b-iq2xxs-q2k.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--ManiacLabs--Qwen3.6-35B-A3B-2bit/snapshots/5f92fade67bd6712b339fad950f86296d1b0a71e/qwen3.6-35b-a3b-iq2xxs-q2k.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Cache size: `12G`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--ManiacLabs--Qwen3.6-35B-A3B-2bit/snapshots/5f92fade67bd6712b339fad950f86296d1b0a71e/qwen3.6-35b-a3b-iq2xxs-q2k.gguf \
  --host 127.0.0.1 \
  --port 18090 \
  --ctx-size 4096 \
  --alias maniac-qwen36-35b-a3b-2bit-gguf \
  --jinja \
  -ngl 999
```

llama.cpp selected `peg-native` chat formatting. During the pilot calls it
reported roughly `42-43` generation tokens per second.

Runtime warning:

```text
n_ctx_seq (4096) < n_ctx_train (262144) -- the full capacity of the model will not be utilized
```

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model maniac-qwen36-35b-a3b-2bit-gguf \
  --base-url http://127.0.0.1:18090/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id maniac-qwen36-35b-a3b-2bit-gguf-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/maniac-qwen36-35b-a3b-2bit-gguf-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Returned empty assistant content. |
| `bfcl-parallel-ticket-routing` | fail | Began a `create_ticket` tool-call fragment and a partial `assign_ticket` fragment, but did not produce strict parseable `<tool_call>...</tool_call>` envelopes. |
| `bfcl-invalid-tool` | fail | Returned empty assistant content. This avoided the forbidden delete token, but did not produce the expected refusal/allowed-tool text. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Keep as a runtime-proven Qwen3.6 35B-A3B 2-bit local comparison point. Future
  repair should focus on a Qwen/Maniac-specific prompt profile before rerunning
  strict BFCL-style endpoint pilots.
