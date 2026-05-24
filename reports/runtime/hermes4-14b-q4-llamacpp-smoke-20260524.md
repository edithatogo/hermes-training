# Hermes 4 14B Q4 llama.cpp Runtime Smoke

Date: 2026-05-24

## Runtime

- Runtime: `/Volumes/PortableSSD/GitHub/llama.cpp/build/bin/llama-server`
- Build: `b1-5d44db6`
- Model alias: `hermes-4-14b-q4`
- Artifact: `/Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4/Hermes-4-14B_Q4_k_m.gguf`
- Artifact size: `9001753248` bytes
- Endpoint: `http://127.0.0.1:8092/v1`
- Context: `4096`
- GPU layers: `auto`

## Load Evidence

llama.cpp loaded the model successfully on the M1 Max:

- Architecture: `qwen3`
- Parameters: `14.77B`
- GGUF type: `Q4_K - Medium`
- File size reported by llama.cpp: `8.38 GiB`
- Projected Metal memory: `9118 MiB`
- Offload: `41/41` layers
- Free device memory after fit: approximately `16440 MiB`

## Smoke

```bash
SMOKE_PROMPT='Return exactly this JSON object and nothing else: {"ok": true}' \
  bash ollama-pack/scripts/runtime_smoke.sh \
  hermes-4-14b-q4 \
  http://127.0.0.1:8092/v1
```

Result: passed.

Latency: `633ms`.

## Decision

Hermes 4 14B Q4 is now proven as a local OpenAI-compatible runtime on the MacBook Pro M1 Max with 32GB unified memory. It is a baseline/runtime target, not a publishable fine-tuned Hermes-agent result.
