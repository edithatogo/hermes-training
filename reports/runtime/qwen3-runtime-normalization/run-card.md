# Runtime Card: Qwen3 Empty-Think Normalization

## Identity

- Runtime feature: empty leading `<think></think>` normalization before Hermes tool parsing
- Date: 2026-05-22
- Scope: local Hermes runtime integration only
- Publication impact: does not change strict benchmark scores

## Contract

The normalizer may remove only empty leading Qwen-style thinking wrappers before JSON or tool-call parsing:

- allowed: `<think></think><tool_call>...</tool_call>`
- allowed: whitespace around an empty leading thinking block
- not allowed: non-empty reasoning blocks
- not allowed: arbitrary prose extraction
- not allowed: changing benchmark strict pass/fail gates

Strict benchmark results remain the model-quality gate. The diagnostic empty-think-stripped score is allowed only to explain whether a runtime parser could recover a response after harmless wrapper removal.

## Implemented Helpers

- `scripts/normalize_tool_response.py`
- `ollama-pack/scripts/normalize_runtime_json.py`

## Validation

```bash
source scripts/env.sh
./.venv/bin/python scripts/normalize_tool_response.py --self-test
./.venv/bin/python ollama-pack/scripts/normalize_runtime_json.py --self-test
```

## Next Runtime Proof

Run an endpoint smoke against an already available local model or SSD-backed artifact:

```bash
ollama-pack/scripts/runtime_smoke.sh <model_name> http://127.0.0.1:11434/v1
```

If using MLX server or LM Studio, keep the same response contract and record the endpoint in a runtime card.
