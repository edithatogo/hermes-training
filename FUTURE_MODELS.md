# Bleeding-Edge Model Radar

This file is the model-selection radar for Hermes fine-tunes on a MacBook Pro M1 Max with 32GB RAM. Refresh it before starting a new track because model availability, MLX support, Ollama converter support, and quantized releases move quickly.

## Selection Rules

- Prefer models with **a real open-weight repository** and a Mac-usable runtime path.
- Separate **inference candidates** from **fine-tune candidates**. A model that fits for inference may still be too tight for local LoRA training.
- Prefer **MLX, Ollama experimental safetensors, or GGUF** for local validation.
- Prefer **adapter-only publication** for large or license-sensitive models.
- Require a runtime proof before training: one prompt through MLX/Ollama/LM Studio and one Hermes prompt through an OpenAI-compatible endpoint.

## Promotion Rules

Use the narrowest gate that proves the role, and do not publish beyond the gate.

| Role | Benchmark gate | Publication limit |
|---|---|---|
| `local-finetune` | Dataset audit, train config, Hermes-local benchmark, and the lane-specific standard benchmark | Adapter-only publication unless the base model license explicitly allows more. |
| `local-runtime` | Runtime proof, endpoint smoke, and Hermes prompt smoke | Runtime card and smoke notes only; no benchmark or adapter publication until promoted. |
| `cloud-teacher` | Teacher-eval gate: compare against a baseline and record the Hermes prompt smoke | Publish model card, comparison notes, and eval summaries only; do not publish adapters or merged weights unless redistribution is explicitly allowed. |
| `cloud-finetune` | Full benchmark gate: dataset audit, train config, token count, loss/memory/runtime summary, Hermes-local benchmark, and the standard benchmark for the lane | Publish adapters and benchmark summaries if the license allows it. |
| `retrieval` | Retrieval gate: retrieval-specific metrics and retrieval smoke, not chat benchmarks | Publish retrieval notes and retrieval artifacts only; do not claim assistant-quality benchmarks. |
| `research-runtime` | Runtime proof only, plus Hermes smoke if the model can be served through an endpoint | Publish runtime evidence only; benchmark claims wait for promotion. |
| `watchlist` | No gate until the model is promoted out of watchlist | Docs/spec notes only; no weights, adapters, or benchmark claims. |

## Practical Frontier For 32GB

| Rank | Family | Candidate | Params | Fit | Role | Notes |
|---|---|---:|---:|---|---|---|
| Watch | Qwen | `Qwen3.7-Max` / `Qwen3.7-Plus-Preview` | not open-weight | Hosted only | Hosted teacher/watchlist | Announced as a new agentic model, but no official Qwen Hugging Face open-weight repo exists yet. Do not build a local track until weights or a supported API workflow are available. |
| 1 | Qwen | `Qwen/Qwen3.6-35B-A3B` | 35B total / 3B active | Inference yes, local fine-tune risky | Primary open-weight frontier runtime target | Official HF repo exists and community GGUF/MLX quants exist; prove runtime on Mac before using as teacher. |
| 2 | Hermes | `NousResearch/Hermes-4-14B` | 14B dense | Inference yes, local LoRA possible but tight | Baseline and calibration target | Already Hermes-style; compare our adapters against this before training larger experiments. |
| 3 | Gemma | `google/gemma-4-26B-A4B-it` | 26B total / 4B active | Inference yes, local fine-tune risky | Multimodal/agentic MoE target | Official HF model exists; GGUF/quant path must be validated for tool-call stability. |
| 4 | Qwen | `Qwen/Qwen3-4B-MLX-4bit` | 4B | Fine-tune yes | First training track | Local training is proven, but strict tool-call formatting needs better target data before scaling. |
| 5 | LFM | `LiquidAI/LFM2.5-1.2B-Instruct` / Thinking | 1.2B | Fine-tune yes | Low-latency helper model | Official card lists llama.cpp, MLX, vLLM support and Unsloth/TRL fine-tuning recipes. |
| 6 | LFM | `LiquidAI/LFM2-8B-A1B` | 8B-ish hybrid | Fine-tune possible, verify | Experimental LFM track | Local Ollama has LFM2 converter changes; validate before long runs. |
| 7 | Ministral | `mlx-community/Ministral-3-8B-Instruct-2512-4bit` | 8B | Fine-tune possible | Apache 2.0 8B baseline | Useful if Qwen/Gemma/LFM tool behavior regresses. |

## Research Frontier

| Family | Candidate | Status | How to Treat It |
|---|---|---|---|
| Qwen3-Next | `Qwen/Qwen3-Next-80B-A3B-Instruct`, Qwen3-Coder-Next | Real HF models/reports exist; local repo has Qwen3Next converter support | Runtime experiment first. Too large for first local fine-tune, but important for subquadratic/linear-attention roadmap. |
| Mamba-3 | Paper/research implementation | Current paper, not a drop-in Hermes model track yet | Watchlist. Add only after weights + Mac runtime + tokenizer are real. |
| RWKV-7 | RWKV-7 Goose / World variants | Real recurrent family with Apache-licensed code/models | Runtime experiment. Tool-calling chat quality must be tested. |
| BitNet b1.58 | Microsoft BitNet / QVAC BitLoRA ecosystem | Real inference ecosystem; fine-tune path emerging | Research track. Do not block core Hermes work on it. |
| Recursive wrappers | RLM-Qwen-style recursive harnesses | Architecture/harness idea more than a simple model checkpoint | Build only after a clear repo and reproducible dataset objective exist. |

## Claims To Treat Carefully

These may be promising, but should not be promoted until verified with an actual model repo and Mac-capable runtime:

- `Kimi K2.6-Mini`
- `MiMo V2.5-Pro`
- `DeepSeek-V4-Flash`
- `SubQ 1M-Preview`
- `LFM 3 Preview`
- `RLM-Qwen3-8B` unless a concrete checkpoint/harness is selected

## LFM Track

Near-term targets:

- `LiquidAI/LFM2.5-1.2B-Instruct`
- `LiquidAI/LFM2.5-1.2B-Thinking`
- `LiquidAI/LFM2-8B-A1B`
- `LiquidAI/LFM2-24B-A2B` only as an inference/runtime experiment on 32GB, not a first fine-tune target.

Use cases:

- Hermes agent routing and short tool plans.
- Structured extraction.
- RAG and background helper workflows.
- Multi-turn personal assistant flows.
- Low-latency local execution.

## Hermes 4 Track

`NousResearch/Hermes-4-14B` should be treated as:

- A **baseline** for evaluating our Hermes-style fine-tunes.
- A **teacher model** for dataset review or distillation candidates where licensing permits.
- A **runtime target** through Ollama/LM Studio GGUF before attempting local LoRA.

Do not immediately fine-tune Hermes 4 locally. First compare Qwen3 4B/LFM2.5 adapters against it on Hermes tool-use prompts.

## Qwen3.6 Track

`Qwen/Qwen3.6-35B-A3B` is the top frontier candidate, but it is not the first local fine-tune target.

Recommended path:

1. Run quantized inference through LM Studio or Ollama if a compatible GGUF exists.
2. Validate KTransformers on Mac only if Apple Silicon support is real in the chosen branch/build.
3. Use it as a teacher/evaluator for Qwen3 4B and LFM2.5 adapters.
4. Attempt local adapter training only after smoke-testing memory with 1K context, batch 1, low LoRA layer count.

## Qwen3.7 Watchlist

As of 2026-05-22, Qwen3.7 should be tracked as a hosted/API watchlist item, not a local model lane:

- Alibaba/Qwen announced Qwen3.7-Max and preview variants for agentic coding, reasoning, and long-horizon tool execution.
- No official Hugging Face open-weight repositories were available under `Qwen/Qwen3.7-*` during local `huggingface_hub` checks.
- Until weights, license, and runtime artifacts exist, Qwen3.7 can only be considered for hosted teacher/evaluator experiments, not local MLX/Ollama/LM Studio training.

Promotion trigger: add a local track only after an official Qwen model repo, quantized Mac runtime path, or clearly supported hosted API workflow is available and documented.

## Recurrent And Subquadratic Track

These are not just "long context" models. The point is lower memory growth and faster inference on long sequences.

Candidate families:

- **Qwen3.6 / Qwen3-Next:** hybrid Gated DeltaNet, MoE, and attention style architectures.
- **Mamba-3:** SSM/MIMO research direction with improved state tracking.
- **RWKV-7:** recurrent/RNN-style language model family.
- **RecurrentGemma / Griffin:** fixed-size recurrent state plus local attention.
- **BitNet b1.58:** ternary-weight frontier that can radically reduce memory pressure.

Acceptance bar:

1. Load locally.
2. Generate coherent chat response.
3. Serve through an OpenAI-compatible endpoint.
4. Pass Hermes JSON/tool-call smoke prompts.
5. Only then create a fine-tune track.

## Tool Compatibility Matrix

| Family | MLX | KTransformers | Ollama safetensors | Ollama GGUF | LM Studio | Notes |
|---|---|---|---|---|---|---|
| Qwen3.6 35B-A3B | Check | Officially named on HF; Mac support must be verified | Check | Likely through community quants | Likely through GGUF | Best frontier runtime target, not first training target. |
| Hermes 4 14B | Check | Not primary | Check | Likely through community quants | Likely through GGUF | Baseline/teacher. |
| Gemma 4 26B-A4B | Emerging | Not primary | Check | Emerging | Emerging | Multimodal MoE; tool-call stability needs testing. |
| Qwen3 4B | Strong | Not needed | Likely | Strong | Strong | Best first local fine-tune. |
| LFM2.5 1.2B | Strong per official card | Not needed | Check | Strong | Strong | Best low-latency helper fine-tune. |
| LFM2 8B-A1B | Check per build | Not needed | Local Ollama has converter work | Improving | Check | Good Hermes agent target. |
| Mamba-3 | Research | No | No | No | No | Watchlist until weights/runtime mature. |
| RWKV-7 | Limited | No | Check | Mixed | Mixed | Tool-call quality must be tested. |
| BitNet | No | No | No | Check separate runtimes | No | Research track, not core pipeline. |

## Quantization And Runtime Notes

| Model | Current note | Status |
|---|---|---|
| `Qwen/Qwen3.6-35B-A3B` | Official HF weights are in Transformers format and the model card lists Transformers, vLLM, SGLang, and KTransformers compatibility. Keep LM Studio/Ollama/GGUF paths as `needs-runtime-proof` until a Mac run is recorded. | `needs-runtime-proof` |
| `NousResearch/Hermes-4-14B` | Official safetensors are published. Treat Transformers as the first known path and keep GGUF / FP8 / community quant paths as runtime candidates until this repo records a smoke result. | `needs-runtime-proof` |
| `google/gemma-4-26B-A4B-it` | Official image-text-to-text safetensors exist. Community GGUF and on-device quants may exist, but Mac runtime support remains `needs-runtime-proof` here. | `needs-runtime-proof` |
| `Qwen/Qwen3-Next-80B-A3B-Instruct` | Official HF weights and a GGUF family are published. Use it as a runtime-experiment target only; it is not a 32GB fine-tune target. | `needs-runtime-proof` |
| `LiquidAI/LFM2.5-1.2B-Instruct` / `Thinking` | Official model card lists day-one support for llama.cpp, MLX, and vLLM. This is the safest local fine-tune lane in the frontier set. | `ready` |
| `microsoft/bitnet-b1.58-2B-4T` | Official HF weights exist, but the native BitNet runtime path still needs an actual repo-specific smoke before we treat it as supported. | `needs-runtime-proof` |
| `BAAI/bge-m3` | Official retrieval model with FlagEmbedding / sentence-transformers usage. Treat as retrieval-only, not a chat quantization target. | `ready` |
| `jinaai/jina-embeddings-v4` | Official multimodal retrieval model. Use Transformers or sentence-transformers and keep it in the retrieval lane. | `needs-runtime-proof` |
| `LiquidAI/LFM2-ColBERT-350M` | Official late-interaction retriever with PyLate / sentence-transformers usage. Retrieval and reranking only; do not treat it as a generation model. | `needs-runtime-proof` |

## Sources Checked

- Qwen/Qwen3.6-35B-A3B model card.
- NousResearch/Hermes-4-14B Hugging Face repo and Hermes 4 technical report.
- google/gemma-4-26B-A4B-it and NVIDIA quantized Gemma 4 26B A4B model cards.
- LiquidAI/LFM2.5 model card and Liquid LEAP fine-tuning docs.
- KTransformers Qwen SFT docs.
- Mamba-3 paper.
- Local Ollama repo converter/runtime support for LFM2, Qwen3Next, Gemma4, safetensors, and MLX runner.
