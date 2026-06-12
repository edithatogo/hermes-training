# LFM2.5 8B A1B Q4_K_M llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`LiquidAI/LFM2.5-8B-A1B-GGUF` was run through the strict Hermes BFCL-style
endpoint pilot using the cached SSD GGUF artifact and Homebrew llama.cpp server.

Result: `0/3` cases passed, pass rate `0.000`.

This is promotion-blocking evidence. The model loads and responds quickly in the
local Mac llama.cpp lane, but it does not emit strict Hermes tool calls.

## Artifact

- Repo: `LiquidAI/LFM2.5-8B-A1B-GGUF`
- File: `LFM2.5-8B-A1B-Q4_K_M.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--LiquidAI--LFM2.5-8B-A1B-GGUF/snapshots/dfd5fdcad7a1c0d31473fb4ca443b8befbacddf0/LFM2.5-8B-A1B-Q4_K_M.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Cache size: `4.8G`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--LiquidAI--LFM2.5-8B-A1B-GGUF/snapshots/dfd5fdcad7a1c0d31473fb4ca443b8befbacddf0/LFM2.5-8B-A1B-Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 18084 \
  --ctx-size 4096 \
  --alias liquid-lfm2-5-8b-a1b-q4km \
  --jinja \
  -ngl 999
```

llama.cpp selected `peg-native` chat formatting. During the short pilot calls it
reported roughly `122-124` generation tokens per second.

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model liquid-lfm2-5-8b-a1b-q4km \
  --base-url http://127.0.0.1:18084/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id lfm25-8b-a1b-q4km-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/lfm25-8b-a1b-q4km-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Refused to use the listed lookup tool and said it lacked database access. |
| `bfcl-parallel-ticket-routing` | fail | Claimed assignment was impossible and emitted prose instead of the two required tool calls. |
| `bfcl-invalid-tool` | fail | Correctly refused the unavailable action, but repeated `delete_customer_record`, which the strict gate forbids. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Keep as an LFM runtime comparison baseline only; any Hermes use would need a
  prompt/profile repair or adapter that proves strict tool-call compliance.
