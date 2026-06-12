# Nemotron 3 Nano 4B Q4_K_M llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` was run through the strict
Hermes BFCL-style local endpoint pilot using llama.cpp.

Result: `0/3` cases passed, pass rate `0.000`.

The runtime path is viable on the MacBook Pro M1 Max, but the model is not
Hermes-compatible under the current strict tool-call contract. It generated
tool-shaped content, but used schemas/wrappers that the Hermes parser does not
accept and leaked forbidden tool text in the invalid-tool case.

## Artifact

- Repo: `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`
- File: `NVIDIA-Nemotron3-Nano-4B-Q4_K_M.gguf`
- Local cache: `/Volumes/PortableSSD/huggingface/hub/models--nvidia--NVIDIA-Nemotron-3-Nano-4B-GGUF/snapshots/ba223d14e45525f7fae81db77ea8cabeb2fc6c25/NVIDIA-Nemotron3-Nano-4B-Q4_K_M.gguf`
- Runtime: llama.cpp `llama-server`
- Server port: `18092`
- Context: `4096`

## Benchmark

```bash
llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--nvidia--NVIDIA-Nemotron-3-Nano-4B-GGUF/snapshots/ba223d14e45525f7fae81db77ea8cabeb2fc6c25/NVIDIA-Nemotron3-Nano-4B-Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 18092 \
  -c 4096 \
  -ngl 999
```

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model nvidia-nemotron-3-nano-4b-q4km \
  --base-url http://127.0.0.1:18092/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id nemotron3-nano-4b-q4km-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/nemotron3-nano-4b-q4km-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Emitted `lookup_customer`-shaped JSON, but wrapped it in `<tool_call>`/`</think>` text and fabricated customer data after the call. |
| `bfcl-parallel-ticket-routing` | fail | Emitted a DSML-style tool-call block that the Hermes parser does not accept. |
| `bfcl-invalid-tool` | fail | Refused the unavailable delete function, but mentioned `delete_customer_record`, violating the strict exclusion rule. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Keep as a prompt/profile or adapter-repair candidate only if Nemotron-specific
  tooling becomes strategically important.
