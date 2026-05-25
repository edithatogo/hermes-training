#!/usr/bin/env bash
set -euo pipefail

# Start Ollama for mem0 read/search work from a clean SSD-backed model root.
# This avoids the older broad model stores that caused Ollama 0.24.0 to hang
# during model-store scanning on this machine.

MODEL_ROOT="${OLLAMA_MODELS:-/Volumes/PortableSSD/Ollama/mem0-clean-models}"
OLLAMA_BIN="${OLLAMA_BIN:-/opt/homebrew/bin/ollama}"
OLLAMA_HOST_VALUE="${OLLAMA_HOST:-127.0.0.1:11434}"

mkdir -p "$MODEL_ROOT"

export OLLAMA_MODELS="$MODEL_ROOT"
export OLLAMA_HOST="$OLLAMA_HOST_VALUE"

exec "$OLLAMA_BIN" serve
