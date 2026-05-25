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
- `scripts/openai_normalizing_proxy.py`
- `ollama-pack/scripts/normalize_runtime_json.py`

## 2026-05-26 lm-eval Bridge Extension

`scripts/openai_normalizing_proxy.py` now also passes through
`/v1/completions` and coerces integer OpenAI `logprobs` requests to boolean
before forwarding to `mlx_lm.server`. This is a compatibility bridge for
`lm_eval --model local-completions`; it does not synthesize loglikelihood
scores and does not make any benchmark claim until a live lm-eval rerun records
raw outputs and a score card.

## Validation

```bash
source scripts/env.sh
./.venv/bin/python scripts/normalize_tool_response.py --self-test
./.venv/bin/python scripts/openai_normalizing_proxy.py --self-test
./.venv/bin/python ollama-pack/scripts/normalize_runtime_json.py --self-test
```

Proxy usage:

```bash
source scripts/env.sh
./.venv/bin/python scripts/openai_normalizing_proxy.py \
  --upstream http://127.0.0.1:11434/v1 \
  --listen-port 8099
```

Point Hermes at `http://127.0.0.1:8099/v1`. Use a different upstream for MLX server or LM Studio as needed.

Live proxy smoke evidence:

- `reports/runtime/openai-normalizing-proxy-ollama-smoke/run-card.md`
- Upstream `http://127.0.0.1:11434/v1`, proxy `http://127.0.0.1:8099/v1`, model `hermes3:8b`, passed `/v1/models` and `/v1/chat/completions`.

The V3 held-out runtime-normalized report is recorded at:

- `/Volumes/PortableSSD/hermes-evals/runtime-normalized-tool-call/qwen3-4b-strict-toolcall-v3-heldout-20260524/summary.md`
- `reports/runtime/qwen3-runtime-normalized-toolcall-v3-heldout/run-card.md`

Result: strict held-out pass `0.250`; runtime-normalized pass `0.875`; residual runtime failure `heldout-argument-correctness-lab-order`.

## Next Runtime Proof

Run an endpoint smoke against an already available local model or SSD-backed artifact:

```bash
ollama-pack/scripts/runtime_smoke.sh <model_name> http://127.0.0.1:11434/v1
```

If using MLX server or LM Studio, keep the same response contract and record the endpoint in a runtime card.
