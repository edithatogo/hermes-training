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
   - For Qwen3 MLX adapters, use a dequantized fused export before llama.cpp conversion when the source model is an MLX 4-bit checkpoint.

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

## Current Qwen3 Runtime Finding

The Qwen3 4B smoke adapter now has three distinct runtime findings:

- MLX server is validated through the OpenAI-compatible `/v1/models` and `/v1/chat/completions` endpoints.
- A dequantized fused export converted successfully to GGUF with llama.cpp, and the `Q4_K_M` GGUF responds correctly through `llama-completion`.
- Ollama is not yet validated for this Qwen3 package. Experimental safetensors import crashes at chat time, and GGUF import drops the Ollama daemon during model creation on this machine.

Artifacts stay on the external SSD:

- Fused dequantized model: `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/merged-dequantized`
- F16 GGUF: `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-f16.gguf`
- Q4_K_M GGUF: `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`

Use LM Studio or direct llama.cpp as the next GGUF validation path before treating Ollama as ready for Qwen3.

## Next Frontier Runtime Candidate

Read-only Hugging Face checks on 2026-05-22 confirmed these next-lane targets. Keep artifacts and notes on `/Volumes/PortableSSD`, and do not add large downloads to this pass:

| Repo | SHA Prefix | Access | Runtime Role |
|---|---|---|---|
| `Qwen/Qwen3.6-35B-A3B` | `995ad96eacd9` | public, ungated, Apache-2.0 tag | Frontier teacher/runtime target; do not local fine-tune first |
| `lmstudio-community/Qwen3.6-35B-A3B-GGUF` | `68a34855558a` | public, ungated, GGUF | First Mac GGUF runtime proof candidate once LM Studio or llama.cpp server is available |
| `unsloth/Qwen3.6-35B-A3B-GGUF` | `a483e9e6cbd5` | public, ungated, GGUF | Alternate quant source; verify exact quant file before download |
| `NousResearch/Hermes-4-14B` | `d6ce765c8b83` | public, ungated | Hermes-aligned baseline/teacher; compare before larger local training |
| `Qwen/Qwen3.7-Max` | hosted preview | hosted API | Hosted-preview watchlist only; no local download or fine-tune lane |
| `Qwen/Qwen3.7-Plus-Preview` | hosted preview | hosted API | Hosted-preview watchlist alias for the same no-download guardrail |

Do not download these large artifacts into the repo. Use `source scripts/env.sh` first so model caches and GGUFs resolve under `/Volumes/PortableSSD`.

## Qwen3.6 / Hermes 4 No-Download Result

Track `qwen36-runtime-proof_20260522` completed the SSD-only runtime proof pass:

- no Qwen3.6 or Hermes 4 local artifact was found on `/Volumes/PortableSSD`
- Ollama, MLX server, and LM Studio default OpenAI-compatible endpoints were not listening
- no runtime smoke was run because doing so would have required a new large model download or an externally provided endpoint
- Qwen3.7 remains hosted-preview watchlist only

The no-download proof is documented in `reports/runtime/qwen36-hermes4-runtime-proof/run-card.md`. The next pass should start from an explicit SSD-backed artifact path or an already-running endpoint, then run the endpoint smoke matrix below.

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
| Qwen3.7-Max / Plus-Preview | Hosted API only | None | Hosted-preview watchlist; do not create a local runtime lane until open weights exist. |
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
