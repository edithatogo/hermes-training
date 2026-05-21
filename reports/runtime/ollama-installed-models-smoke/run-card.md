# Runtime Run Card: Local Ollama Installed Models Smoke

## Identity

- Run name: `ollama-installed-models-smoke`
- Date: 2026-05-22
- Operator: Codex
- Platform lane: Mac local Ollama runtime
- Runtime: Ollama OpenAI-compatible endpoint
- Base endpoint: `http://127.0.0.1:11434/v1`
- Scope: already-installed local Ollama models only; no model pulls

## Installed Model Check

Command:

```bash
ollama list
```

Result:

| Model | ID | Size | Modified |
|---|---:|---:|---|
| `hermes3:8b` | `4f6b83f30b62` | 4.7 GB | 8 days ago |
| `sam860/LFM2:2.6b` | `9db0c3bfa56e` | 1.8 GB | 8 days ago |
| `nomic-embed-text:latest` | `0a109f422b47` | 274 MB | 8 days ago |

The smoke pass used only `hermes3:8b` and `sam860/LFM2:2.6b`. The embedding model was not part of the chat runtime smoke.

OpenAI-compatible model discovery:

```bash
curl -sS --max-time 3 http://127.0.0.1:11434/v1/models
```

Result: endpoint returned `hermes3:8b`, `sam860/LFM2:2.6b`, and `nomic-embed-text:latest`.

## JSON Smoke Matrix

Smoke prompt:

```text
Return exactly this JSON object and nothing else: {"ok": true}
```

| Model | Command | Result | Chat Latency |
|---|---|---:|---:|
| `hermes3:8b` | `source scripts/env.sh && SMOKE_PROMPT='Return exactly this JSON object and nothing else: {"ok": true}' bash ollama-pack/scripts/runtime_smoke.sh 'hermes3:8b' http://127.0.0.1:11434/v1` | Passed | 11776 ms |
| `sam860/LFM2:2.6b` | `source scripts/env.sh && SMOKE_PROMPT='Return exactly this JSON object and nothing else: {"ok": true}' bash ollama-pack/scripts/runtime_smoke.sh 'sam860/LFM2:2.6b' http://127.0.0.1:11434/v1` | Passed | 3261 ms |

The script validated both `/v1/models` visibility and `/v1/chat/completions` assistant content as strict JSON with `ok=true`.

## Environment

```bash
ollama --version
uname -a
```

Results:

- Ollama: `0.24.0`
- Host: `Darwin Pleiades-M1-14-MBP.local 25.3.0 ... RELEASE_ARM64_T6000 arm64`

## Limitations

- This run proves only that the currently installed Ollama models are reachable through the local OpenAI-compatible endpoint and can return strict JSON for the smoke prompt.
- No model was pulled, created, converted, or modified.
- `nomic-embed-text:latest` was discovered but not validated as a chat model.
- Latency is a single smoke measurement per model, not a benchmark.
- The run does not validate Hermes application wiring beyond the endpoint surface that Hermes uses: `/v1/models` and `/v1/chat/completions`.
