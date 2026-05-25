# Runtime Targets

The project should not bet on one serving tool. The acceptance target is: a fine-tuned model can be used by Hermes through at least one local OpenAI-compatible endpoint, and preferably through both Ollama and a GGUF-compatible desktop tool.

mem0 has its own runtime rules in [mem0/RUNTIME_TARGETS.md](./mem0/RUNTIME_TARGETS.md). In short: chat/extraction models can use OpenAI-compatible chat endpoints, but embedding and retriever candidates also need embedding, reranking, or `POST /retrieve` APIs. Do not assume a Hermes chat runtime is automatically a mem0 embedding runtime.

The format ladder lives in [RUNTIME_FORMAT_LANES.yaml](./RUNTIME_FORMAT_LANES.yaml). GGUF is the portability lane for llama.cpp, LM Studio, and Ollama compatibility; it is not the canonical training format. Train and adapt in MLX, PEFT/safetensors, Unsloth, LEAP/LFM, or a native specialist runtime when that is the stronger path, then export to GGUF only when broad local serving is the goal.

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
   - Start with `mlx_lm.server --model <path_to_model_or_hf_repo>` and point Hermes at the selected OpenAI-compatible port.
   - Default examples often use `http://127.0.0.1:8080/v1`; the recorded Qwen3 smoke proof used `http://127.0.0.1:8088/v1`.

5. **LM Studio**
   - Use GGUF exports.
   - Start the local server with `lms server start --port 1234` or use the LM Studio UI, then point Hermes at `http://localhost:1234/v1`.

6. **KTransformers**
   - Candidate runtime for large sparse Qwen MoE models such as Qwen3.6.
   - Treat as experimental on Apple Silicon until the selected branch/build passes a local prompt and OpenAI-compatible endpoint smoke test.

7. **Native specialist runtimes**
   - Use RWKV, BitNet, Mamba/SSM, recursive/RLM, LEAP/LFM, or KTransformers-native launchers when the model family depends on them.
   - Record an invocation or endpoint wrapper contract before treating the runtime as Hermes-compatible.

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

Use LM Studio as the remaining desktop GGUF validation path before treating the Qwen3 GGUF package as fully proven. Direct llama.cpp already passed for the Q4_K_M artifact.

## Next Frontier Runtime Candidate

Read-only Hugging Face checks on 2026-05-22 confirmed these next-lane targets. Keep artifacts and notes on `/Volumes/PortableSSD`, and do not add large downloads to this pass:

| Repo | SHA Prefix | Access | Runtime Role |
|---|---|---|---|
| `Qwen/Qwen3.6-35B-A3B` | `995ad96eacd9` | public, ungated, Apache-2.0 tag | Frontier teacher/runtime target; do not local fine-tune first |
| `lmstudio-community/Qwen3.6-35B-A3B-GGUF` | `68a34855558a` | public, ungated, GGUF | First Mac GGUF runtime proof candidate once LM Studio or llama.cpp server is available |
| `unsloth/Qwen3.6-35B-A3B-GGUF` | `a483e9e6cbd5` | public, ungated, GGUF | Alternate quant source; verify exact quant file before download |
| `NousResearch/Hermes-4-14B` | `d6ce765c8b83` | public, ungated | Hermes-aligned baseline/teacher; compare before larger local training |
| `NousResearch/Hermes-4.3-36B` | verify exact repo revision before use | public model card, no local artifact found | Newer Hermes baseline/teacher candidate; runtime proof needed |

Do not download these large artifacts into the repo. Use `source scripts/env.sh` first so model caches and GGUFs resolve under `/Volumes/PortableSSD`.

## Qwen3.6 / Hermes 4 No-Download Result

Track `qwen36-runtime-proof_20260522` completed the SSD-only runtime proof pass:

- no Qwen3.6 or Hermes 4 local artifact was found on `/Volumes/PortableSSD`
- Ollama, MLX server, and LM Studio default OpenAI-compatible endpoints were not listening
- no runtime smoke was run because doing so would have required a new large model download or an externally provided endpoint
- Qwen3.7 was not verified in official public sources and has no local lane

The no-download proof is documented in `reports/runtime/qwen36-hermes4-runtime-proof/run-card.md`. The next pass should start from an explicit SSD-backed artifact path or an already-running endpoint, then run the endpoint smoke matrix below.

## Qwen3.6 Q4_K_M Runtime Result

The follow-up artifact acquisition and proof completed on 2026-05-25:

- Artifact: `/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4/Qwen3.6-35B-A3B-Q4_K_M.gguf`
- Size: `21166757888` bytes
- Runtime proof: `reports/runtime/qwen36-35b-a3b-q4-llamacpp-proof-20260525.md`
- Held-out strict tool-call pass: `0.000`
- Decision: valid llama.cpp runtime proof and frontier baseline only; not promotion-ready for Hermes-agent tool use.

## Installed Ollama Smoke

The installed Ollama models `hermes3:8b` and `sam860/LFM2:2.6b` passed the OpenAI-compatible JSON smoke on 2026-05-22 with no downloads. The run card is `reports/runtime/ollama-installed-models-smoke/run-card.md`.

This proves the local Ollama endpoint remains usable for already-installed Hermes-style and LFM-family models. It does not validate the Qwen3 adapter package, which still needs LM Studio or Ollama import proof from the SSD-backed GGUF.

## Endpoint Smoke Matrix

| Runtime | Start Command | Endpoint | Smoke Check |
|---|---|---|---|
| MLX server | `mlx_lm.server --model <path_to_model_or_hf_repo> --port <port>` | `http://127.0.0.1:<port>/v1` | `GET /v1/models` plus a parseable `POST /v1/chat/completions` response; Qwen3 proof used port `8088` |
| Ollama | `ollama launch hermes` | `http://127.0.0.1:11434/v1` | Hermes picker sees the model and the OpenAI-compatible chat endpoint responds |
| LM Studio | `lms server start --port 1234` | `http://localhost:1234/v1` | OpenAI-compatible chat endpoint responds from the active desktop server |
| Ollama experimental safetensors | `ollama create --experimental -f <Modelfile>` then `ollama launch hermes` | `http://127.0.0.1:11434/v1` | Experimental create succeeds and Hermes can call the model |
| Specialist runtime | `<runtime-specific launcher>` | `<OpenAI-compatible endpoint>` | Record a lane-specific launcher and still require parseable `/v1/models` plus chat completion output |

## Memory And Embedding Runtime Matrix

| Role | Preferred local runtime | Fallback | Required proof |
|---|---|---|---|
| mem0 extractor | Ollama chat endpoint | LM Studio, MLX server, llama.cpp server | `mem0 status` plus add/search benchmark |
| dense embedder | Ollama embeddings | sentence-transformers, Transformers, LM Studio embeddings if exposed | dimension-specific collection and recall benchmark |
| reranker | Transformers or MLX wrapper | endpoint service | rerank benchmark over fixed candidate sets |
| late-interaction retriever | dedicated ColBERT-style service | FAISS/service fallback | `GET /health`, `POST /retrieve`, Recall@k/nDCG/MRR |

## Normalizing Proxy

For local Hermes use, `scripts/openai_normalizing_proxy.py` can sit in front of any non-streaming OpenAI-compatible endpoint and remove only empty leading Qwen `<think></think>` wrappers from `choices[].message.content`.

Examples:

```bash
# Ollama upstream
source scripts/env.sh
./.venv/bin/python scripts/openai_normalizing_proxy.py \
  --upstream http://127.0.0.1:11434/v1 \
  --listen-port 8099

# MLX server upstream, matching the recorded Qwen3 proof port
./.venv/bin/python scripts/openai_normalizing_proxy.py \
  --upstream http://127.0.0.1:8088/v1 \
  --listen-port 8099

# LM Studio upstream
./.venv/bin/python scripts/openai_normalizing_proxy.py \
  --upstream http://127.0.0.1:1234/v1 \
  --listen-port 8099
```

Point Hermes at `http://127.0.0.1:8099/v1`. Streaming chat completions are rejected until SSE normalization has its own contract. This proxy is runtime integration infrastructure; it does not change strict benchmark scoring or Hugging Face publication gates.

## Frontier Runtime Candidates

| Model | First Try | Fallback | Notes |
|---|---|---|---|
| Qwen3.6-35B-A3B | LM Studio/Ollama GGUF or KTransformers | Transformers on CPU/MPS for smoke only | Verify memory at realistic context before using with Hermes. |
| Hermes-4-14B | Ollama/LM Studio GGUF | Transformers | Use as baseline/teacher before local LoRA. |
| Gemma-4-26B-A4B | Ollama/LM Studio GGUF | Transformers | Validate tool-call stability; MoE quant support is moving quickly. |
| LFM2.5-1.2B | MLX/GGUF | LEAP/Unsloth/TRL for training | Best low-latency helper model track. |
| LFM2.5-350M / VL-450M / Audio-1.5B | MLX/GGUF/ONNX/LEAP depending on modality | Defer until use case proof | Verified public LFM2.5 family entries; separate chat, vision, and audio lanes. |
| Mamba-3/RWKV7/BitNet/RLM | Native family runtime | None | Research only until OpenAI-compatible serving is proven. |

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
