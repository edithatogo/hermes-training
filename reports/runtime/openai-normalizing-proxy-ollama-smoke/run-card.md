# Runtime Card: OpenAI Normalizing Proxy Ollama Smoke

Date: 2026-05-24

## Scope

Validate `scripts/openai_normalizing_proxy.py` as a Hermes-facing OpenAI-compatible endpoint in front of an already-installed Ollama model.

## Command

Proxy:

```bash
source scripts/env.sh
./.venv/bin/python scripts/openai_normalizing_proxy.py \
  --upstream http://127.0.0.1:11434/v1 \
  --listen-port 8099 \
  --quiet
```

Smoke:

```bash
source scripts/env.sh
SMOKE_PROMPT='Return exactly this JSON object and nothing else: {"ok": true}' \
  bash ollama-pack/scripts/runtime_smoke.sh 'hermes3:8b' http://127.0.0.1:8099/v1
```

## Result

- Upstream: `http://127.0.0.1:11434/v1`
- Proxy endpoint: `http://127.0.0.1:8099/v1`
- Model: `hermes3:8b`
- `/v1/models`: passed
- `/v1/chat/completions`: passed
- Chat latency: `13701ms`

## Boundary

This smoke proves the proxy can front a live local Ollama endpoint and preserve the OpenAI-compatible surface Hermes needs. It does not validate Qwen3 adapter quality and does not affect Hugging Face publication gates.
