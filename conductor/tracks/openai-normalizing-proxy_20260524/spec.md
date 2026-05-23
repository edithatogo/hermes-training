# Specification: OpenAI Normalizing Proxy

## Overview

Provide a local OpenAI-compatible proxy for Hermes that can sit in front of Ollama, LM Studio, or MLX server and remove only empty leading Qwen `<think></think>` wrappers from non-streaming chat-completion responses.

## Requirements

- Support `GET /v1/models`.
- Support non-streaming `POST /v1/chat/completions`.
- Forward authorization and ordinary request headers to the upstream endpoint.
- Normalize only `choices[].message.content` values by stripping empty leading thinking wrappers.
- Reject streaming chat completions until SSE normalization has an explicit contract.
- Expose a self-test that proves model discovery, chat normalization, and streaming rejection.
- Document usage as runtime integration only, not benchmark publication evidence.

## Acceptance Criteria

- `scripts/openai_normalizing_proxy.py --self-test` passes.
- Project readiness validation passes.
- Runtime docs include an example for Ollama, LM Studio, and MLX server.
