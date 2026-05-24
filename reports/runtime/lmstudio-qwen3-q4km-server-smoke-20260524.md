# LM Studio Qwen3 Q4_K_M Runtime Smoke

Date: 2026-05-24

## Runtime

- App: `/Applications/LM Studio.app`
- Version: `0.4.14+4`
- CLI: `/opt/homebrew/bin/lms` -> `/Applications/LM Studio.app/Contents/Resources/app/.webpack/lms`
- Server: `http://127.0.0.1:1234/v1`
- Model identifier: `qwen3-4b-hermes-smoke-q4_K_M`
- Artifact: `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`
- LM Studio model entry: `/Users/doughnut/.lmstudio/models/hermes-local/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`
- Storage mode: symbolic link to the SSD artifact, not a copied model file

## Setup Commands

```bash
open -a 'LM Studio'
lms server start
lms import -l -y \
  --user-repo hermes-local/qwen3-4b-hermes-smoke \
  /Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf
lms load qwen3-4b-hermes-smoke \
  --identifier qwen3-4b-hermes-smoke-q4_K_M \
  --context-length 4096 \
  --gpu max \
  -y
```

## Smoke

```bash
SMOKE_PROMPT='Return exactly this JSON object and nothing else: {"ok": true}' \
  bash ollama-pack/scripts/runtime_smoke.sh \
  qwen3-4b-hermes-smoke-q4_K_M \
  http://127.0.0.1:1234/v1
```

Result: passed.

Latency: `7954ms`.

## Decision

The LM Studio blocker is cleared for the existing Qwen3 Q4_K_M GGUF. LM Studio now provides a second local OpenAI-compatible runtime path alongside llama.cpp.
