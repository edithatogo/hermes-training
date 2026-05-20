# Runtime Targets

The project should not bet on one serving tool. The acceptance target is: a fine-tuned model can be used by Hermes through at least one local OpenAI-compatible endpoint, and preferably through both Ollama and a GGUF-compatible desktop tool.

## Preferred Order

1. **Ollama via `ollama launch hermes`**
   - Best user experience when the model is visible to Ollama.
   - Hermes is configured against `http://127.0.0.1:11434/v1`.
   - Use this for daily operation.

2. **Ollama experimental safetensors/MLX path**
   - The local Ollama repo now includes an MLX runner and experimental safetensors creation path.
   - Useful when a model can stay in HF safetensors format and avoid a GGUF conversion step.
   - Treat as experimental until a model-specific smoke test passes.

3. **Ollama GGUF path**
   - Most portable local path.
   - Required when LM Studio compatibility matters.
   - Use `Q4_K_M` by default for 8B-ish models on 32GB; consider `Q5_K_M` only after memory checks.

4. **MLX server**
   - Fastest Mac-first fallback for MLX-compatible models and adapters.
   - Start with `mlx_lm.server --model <path_to_model_or_hf_repo>` and point Hermes at `http://127.0.0.1:8080/v1`.

5. **LM Studio**
   - Use GGUF exports.
   - Start the local server with `lms server start --port 1234` or use the LM Studio UI, then point Hermes at `http://localhost:1234/v1`.

6. **KTransformers**
   - Candidate runtime for large sparse Qwen MoE models such as Qwen3.6.
   - Treat as experimental on Apple Silicon until the selected branch/build passes a local prompt and OpenAI-compatible endpoint smoke test.

## Ollama Notes From Local Repo

The local `/Users/doughnut/GitHub/ollama` tree includes newer support that should influence packaging:

- `cmd/launch/hermes.go` configures Hermes through Ollama's OpenAI-compatible endpoint and model picker.
- `runner/runner.go` can dispatch `--mlx-engine` to `x/mlxrunner`.
- Integration tests exercise `ollama create --experimental -f <Modelfile>` for safetensors model directories.
- Converters exist for newer families including Gemma4, Gemma3n, LFM2, Qwen3, Qwen3Next, and Qwen3-VL.
- A recent local commit adjusts LFM2 output norm tensor naming in llama.cpp.

## Runtime Card Template

Use [`templates/runtime/runtime-card.md`](./templates/runtime/runtime-card.md) for every runtime or model run card. The card should capture the exact runtime, model, command, endpoint, smoke prompt, result, and limitations.

## Endpoint Smoke Matrix

| Runtime | Start Command | Endpoint | Smoke Check |
|---|---|---|---|
| MLX server | `mlx_lm.server --model <path_to_model_or_hf_repo>` | `http://127.0.0.1:8080/v1` | `GET /v1/models` plus a parseable `POST /v1/chat/completions` response |
| Ollama | `ollama launch hermes` | `http://127.0.0.1:11434/v1` | Hermes picker sees the model and the OpenAI-compatible chat endpoint responds |
| LM Studio | `lms server start --port 1234` | `http://localhost:1234/v1` | OpenAI-compatible chat endpoint responds from the active desktop server |
| Ollama experimental safetensors | `ollama create --experimental -f <Modelfile>` then `ollama launch hermes` | `http://127.0.0.1:11434/v1` | Experimental create succeeds and Hermes can call the model |
| Specialist runtime | `<runtime-specific launcher>` | `<OpenAI-compatible endpoint>` | Record a lane-specific launcher and still require parseable `/v1/models` plus chat completion output |

## Frontier Runtime Candidates

| Model | First Try | Fallback | Notes |
|---|---|---|---|
| Qwen3.6-35B-A3B | LM Studio/Ollama GGUF or KTransformers | Transformers on CPU/MPS for smoke only | Verify memory at realistic context before using with Hermes. |
| Hermes-4-14B | Ollama/LM Studio GGUF | Transformers | Use as baseline/teacher before local LoRA. |
| Gemma-4-26B-A4B | Ollama/LM Studio GGUF | Transformers | Validate tool-call stability; MoE quant support is moving quickly. |
| LFM2.5-1.2B | MLX/GGUF | LEAP/Unsloth/TRL for training | Best low-latency helper model track. |
| Mamba-3/RWKV/BitNet | Native family runtime | None | Research only until OpenAI-compatible serving is proven. |

## Runtime Acceptance Tests

For every promoted adapter/runtime package, including specialist lanes that expose an OpenAI-compatible endpoint:

```bash
curl http://127.0.0.1:11434/v1/models
curl http://127.0.0.1:11434/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"MODEL_NAME","messages":[{"role":"user","content":"Return JSON with key ok set to true."}],"temperature":0}'
```

Then launch Hermes:

```bash
ollama launch hermes
```

Validate:

- Hermes sees the model in its picker.
- Tool-call prompts preserve the expected schema.
- JSON-mode prompts remain parseable.
- Multi-turn memory does not corrupt chat formatting.
- Specialist lanes must be recorded with a dedicated run card if the launcher or endpoint differs from Ollama, MLX, or LM Studio defaults.

## Packaging Rules

- Keep adapters and model weights out of Git.
- Publish adapters to Hugging Face with exact base model and commit metadata.
- Publish GGUF artifacts only when the license permits redistribution.
- Prefer adapter-only releases for models with restrictive or unclear redistribution terms.
- Record the exact runtime used for validation: MLX server, Ollama safetensors, Ollama GGUF, or LM Studio.
- Keep merged models, GGUF exports, and packaged artifacts on SSD-backed paths such as `/Volumes/PortableSSD`.
