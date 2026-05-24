# llama.cpp Qwen3 Q4_K_M Runtime Smoke

Date: 2026-05-24

## Runtime

- Binary: `/Volumes/PortableSSD/GitHub/llama.cpp/build/bin/llama-server`
- Build: `b1-5d44db6`
- Model: `qwen3-4b-hermes-smoke-q4_K_M`
- Artifact: `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`
- Endpoint: `http://127.0.0.1:8091/v1`
- Context: `4096`
- GPU layers: `auto`
- SSD run card: `/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/llamacpp-qwen3-q4km-server-smoke-20260524.md`

## Build Note

`llama-server` was not present initially. Building the target required a local toolchain patch in `/Volumes/PortableSSD/GitHub/llama.cpp/tools/server/server-http.h` to include `<unordered_map>`. The llama.cpp repository already had unrelated local changes and untracked files, so that external working tree was not committed from this repo.

## Smoke

```bash
SMOKE_PROMPT='Return exactly this JSON object and nothing else: {"ok": true}' \
  bash ollama-pack/scripts/runtime_smoke.sh \
  qwen3-4b-hermes-smoke-q4_K_M \
  http://127.0.0.1:8091/v1
```

Result: passed.

Latency: `5296ms`.

## Model Endpoint

`GET /v1/models` returned the alias `qwen3-4b-hermes-smoke-q4_K_M` with GGUF metadata:

- `n_ctx`: `4096`
- `n_ctx_train`: `65536`
- `n_params`: `4022468096`
- `size`: `2491323904`
- owner: `llamacpp`

## Decision

This completes a local, SSD-backed, OpenAI-compatible GGUF serving path that does not depend on LM Studio. LM Studio remains useful as a target runtime, but it is not required to prove this artifact.
