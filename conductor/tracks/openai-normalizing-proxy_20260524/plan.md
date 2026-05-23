# Plan: OpenAI Normalizing Proxy

## Phase 1 - Proxy Implementation

- [x] Task: Add OpenAI-compatible normalizing proxy script.
- [x] Task: Add self-test covering `/v1/models`, `/v1/chat/completions`, and streaming rejection.

## Phase 2 - Documentation And Validation

- [x] Task: Document proxy usage for Ollama, LM Studio, and MLX server.
- [x] Task: Run syntax, self-test, and readiness validation.
- [x] Task: Record publication boundary.
- [x] Task: Run live Ollama smoke through the proxy.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10.
- Evidence: proxy self-test covers `/v1/models`, normalized non-streaming `/v1/chat/completions`, and streaming rejection; live Ollama smoke passed through `http://127.0.0.1:8099/v1` with `hermes3:8b`; docs route Hermes to the proxy endpoint; publication docs keep strict raw scoring as the gate.
