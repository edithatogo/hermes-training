# Hermes Shortlist Mac/Metal Parity - 2026-06-12

This report records the current local Mac/Metal proof slice for the Hermes shortlist. It distinguishes a passing mainline adapter smoke from blocked helper-lane endpoint contracts.

## Successful Mainline Path

| Model | Runtime | Command | Result |
|---|---|---|---|
| `Qwen/Qwen3-4B-MLX-4bit` | MLX server | `python -m mlx_lm.server --model Qwen/Qwen3-4B-MLX-4bit --adapter-path gemma4/experiments/qwen3-4b-strict-toolcall-v3-no-think/lora_adapter --host 127.0.0.1 --port 8088` plus `ollama-pack/scripts/runtime_smoke.sh` | Passed. `/v1/models` and `/v1/chat/completions` responded, strict JSON parsed, chat latency was `2922ms`. |
| `Qwen3-4B-Hermes` GGUF | llama.cpp | `/opt/homebrew/bin/llama-completion -m /Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf -p '/no_think Return exactly this JSON object and nothing else: {"ok": true}' -n 32 --temp 0 --ctx-size 4096` | Passed. The GGUF returned `{"ok": true}` and reported `313.99ms` total time. |

## Blocked Helper Lanes

| Model | Runtime | Command | Result |
|---|---|---|---|
| `Qwen/Qwen3.5-0.8B` | MLX server | `python -m mlx_lm.server --model Qwen/Qwen3.5-0.8B --host 127.0.0.1 --port 8098` plus `ollama-pack/scripts/runtime_smoke.sh` | Blocked. The model loaded and `/v1/models` responded, but the chat smoke returned no assistant content under the strict JSON prompt. |
| `Qwen/Qwen3.5-2B` | MLX server | `python -m mlx_lm.server --model Qwen/Qwen3.5-2B --host 127.0.0.1 --port 8099` plus `ollama-pack/scripts/runtime_smoke.sh` | Blocked. The model loaded and `/v1/models` responded, but the chat smoke never completed cleanly; the run was interrupted after the endpoint contract failed to resolve. |

## Interpretation

- The Mac/Metal path is still valid for the Qwen3 4B MLX adapter target.
- The same mainline target also remains valid through llama.cpp GGUF, which is the current portable local runtime lane.
- The smaller Qwen3.5 helper lanes currently fail the strict chat contract on this endpoint shape, so they remain helper/extraction candidates rather than promotion candidates.
- The failure mode is useful evidence: these models load, but prompt/contract compatibility is not yet good enough for strict Hermes promotion.

## Follow-Up

- Keep the mainline Qwen3 4B MLX adapter as the current local fine-tune target.
- Keep Qwen3.5 0.8B and 2B in the `tiny-helper-no-prefill` lane until the strict chat contract is repaired.
- Leave Ollama/LM Studio parity evidence in the existing runtime cards; use this report as the current Mac/Metal checkpoint for the shortlist phase.
