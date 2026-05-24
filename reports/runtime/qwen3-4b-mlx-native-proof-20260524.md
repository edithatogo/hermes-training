# Qwen3 4B MLX Native Runtime Proof

Date: 2026-05-24

## Target

- Format lane: `mlx-native`
- Model: `Qwen/Qwen3-4B-MLX-4bit`
- Cached revision: `52a5ab34fa604bc8af6d3ce0cac0cab10b7eb495`
- Artifact path: `/Volumes/PortableSSD/huggingface/hub/models--Qwen--Qwen3-4B-MLX-4bit/snapshots/52a5ab34fa604bc8af6d3ce0cac0cab10b7eb495`
- Runtime: `mlx_lm.server`
- Endpoint: `http://127.0.0.1:8094/v1`

## Command

```bash
source scripts/env.sh
./.venv/bin/python -m mlx_lm.server \
  --model /Volumes/PortableSSD/huggingface/hub/models--Qwen--Qwen3-4B-MLX-4bit/snapshots/52a5ab34fa604bc8af6d3ce0cac0cab10b7eb495 \
  --host 127.0.0.1 \
  --port 8094
```

## Runtime Smoke

```bash
SMOKE_PROMPT='/no_think Return exactly this JSON object and nothing else: {"ok": true}' \
  bash ollama-pack/scripts/runtime_smoke.sh \
  Qwen/Qwen3-4B-MLX-4bit \
  http://127.0.0.1:8094/v1
```

Result:

- `/v1/models`: passed
- `/v1/chat/completions`: passed
- Chat latency: `3347ms`
- Smoke output: `/Volumes/PortableSSD/hermes-evals/runtime-format-lanes/mlx-native/qwen3-4b-mlx-native-smoke/smoke-20260524.txt`

## Held-Out Tool-Call Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_tool_call_benchmark.py \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --base-url http://127.0.0.1:8094/v1 \
  --user-prefix /no_think \
  --run-id qwen3-4b-mlx-native-heldout-nothink-20260524 \
  --output-dir /Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-4b-mlx-native-heldout-nothink-20260524
```

Result:

| Metric | Value |
|---|---:|
| Cases | 8 |
| Passed | 2 |
| Strict pass rate | 0.250 |
| Tool-call JSON-valid rate | 0.000 |
| Argument accuracy rate | 0.000 |
| Invalid-tool handling rate | 1.000 |
| Multi-turn repair rate | 0.000 |

Raw output:

`/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-4b-mlx-native-heldout-nothink-20260524`

## Decision

This is a valid MLX-native runtime proof, not a promotion. The endpoint is usable through an OpenAI-compatible server, but the held-out strict tool-call score is below the publication gate and below the current best local LM Studio Qwen3 GGUF endpoint.

Keep `Qwen/Qwen3-4B-MLX-4bit` as a Mac-local harness/regression baseline. Do not publish model-improvement claims from this proof.
