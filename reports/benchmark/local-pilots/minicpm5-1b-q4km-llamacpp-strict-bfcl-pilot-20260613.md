# MiniCPM5 1B Q4_K_M llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`openbmb/MiniCPM5-1B-GGUF` was run through the strict Hermes BFCL-style
endpoint pilot using the cached SSD GGUF artifact and Homebrew llama.cpp server.

Result: `0/3` cases passed, pass rate `0.000`.

This is promotion-blocking evidence. The model loads cleanly and is fast enough
for the local Mac runtime lane, but it emits tool-shaped text rather than
Hermes/OpenAI tool-call JSON and fails the invalid-tool guard.

## Artifact

- Repo: `openbmb/MiniCPM5-1B-GGUF`
- File: `MiniCPM5-1B-Q4_K_M.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--openbmb--MiniCPM5-1B-GGUF/snapshots/87007042419d30c1d8f38ef065424ee33870831e/MiniCPM5-1B-Q4_K_M.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Cache size: `662M`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--openbmb--MiniCPM5-1B-GGUF/snapshots/87007042419d30c1d8f38ef065424ee33870831e/MiniCPM5-1B-Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 18085 \
  --ctx-size 4096 \
  --alias minicpm5-1b-q4km \
  --jinja \
  -ngl 999
```

llama.cpp selected `peg-native` chat formatting. During the pilot calls it
reported roughly `193-204` generation tokens per second.

Runtime warning:

```text
n_ctx_seq (4096) < n_ctx_train (131072) -- the full capacity of the model will not be utilized
```

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model minicpm5-1b-q4km \
  --base-url http://127.0.0.1:18085/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id minicpm5-1b-q4km-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/minicpm5-1b-q4km-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Emitted `name="lookup_customer"` text with the customer id, but no parseable tool call. |
| `bfcl-parallel-ticket-routing` | fail | Emitted one partial `create_ticket`-shaped text fragment, not the two required strict tool calls. |
| `bfcl-invalid-tool` | fail | Mentioned the forbidden `delete_customer_record` function and then emitted lookup-shaped text. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Keep only as a tiny local runtime comparison lane unless a future prompt
  profile or adapter explicitly repairs strict tool-use behavior.
