# Nanbeige 4.1 3B Q4_K_M llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`Mungert/Nanbeige4.1-3B-GGUF` was run through the strict Hermes BFCL-style
endpoint pilot using the cached SSD GGUF artifact and Homebrew llama.cpp
server.

Result: `0/3` cases passed, pass rate `0.000`.

The model loaded and generated quickly, but every strict pilot case returned
empty assistant content. This makes it a runtime-proven local comparison point,
not a Hermes tool-call candidate without prompt/profile repair.

## Artifact

- Repo: `Mungert/Nanbeige4.1-3B-GGUF`
- File: `Nanbeige4.1-3B-q4_k_m.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--Mungert--Nanbeige4.1-3B-GGUF/snapshots/7a35d8054f29ebe6fecc7e54b2b2e313e4307e63/Nanbeige4.1-3B-q4_k_m.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Cache size: `2.4G`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--Mungert--Nanbeige4.1-3B-GGUF/snapshots/7a35d8054f29ebe6fecc7e54b2b2e313e4307e63/Nanbeige4.1-3B-q4_k_m.gguf \
  --host 127.0.0.1 \
  --port 18091 \
  --ctx-size 4096 \
  --alias nanbeige41-3b-q4km \
  --jinja \
  -ngl 999
```

llama.cpp selected `peg-native` chat formatting. During the pilot calls it
reported roughly `71-72` generation tokens per second.

Runtime warning:

```text
n_ctx_seq (4096) < n_ctx_train (262144) -- the full capacity of the model will not be utilized
```

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model nanbeige41-3b-q4km \
  --base-url http://127.0.0.1:18091/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id nanbeige41-3b-q4km-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/nanbeige41-3b-q4km-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Returned empty assistant content. |
| `bfcl-parallel-ticket-routing` | fail | Returned empty assistant content. |
| `bfcl-invalid-tool` | fail | Returned empty assistant content; avoided forbidden text but did not produce the expected refusal/allowed-tool response. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Keep as a fast local runtime comparison point only. Any follow-up should
  first test a Nanbeige-specific chat/prompt profile.
