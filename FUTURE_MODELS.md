# Bleeding-Edge Model Radar

This file is the model-selection radar for Hermes fine-tunes on a MacBook Pro M1 Max with 32GB RAM. Refresh it before starting a new track because model availability, MLX support, Ollama converter support, and quantized releases move quickly.

Latest scans:

- [Current release scan](./reports/model-radar/current-release-scan-20260524.md)
- [Qwen3.7/Qwen3.6/Hermes 4 availability check](./reports/model-radar/qwen37-qwen36-hermes4-check-20260524.md)

2026-05-26 refresh: no official Qwen3.7 open-weight lane was verified. The
only new actionable delta is Qwen3.6 GGUF packaging with bundled MTP /
self-speculative decoding heads, especially
`mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF` and
`localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF`. Treat these as runtime latency
experiments behind the existing Qwen3.6 Q4_K_M proof, not local fine-tune
targets.

No official Qwen3.7 open-weight local lane was verified. Qwen3.7-Max/Plus should be treated as API/preview/proprietary until official weights or a supported hosted workflow are verified.

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
| 1 | Qwen | `Qwen/Qwen3.6-35B-A3B`, `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX`, `deepsweet/Qwen3.6-35B-A3B-MLX-oQ4`, MTP GGUF packages | 35B total / 3B active | Inference yes, local fine-tune risky | Primary open-weight frontier runtime target | Official HF repo and MLX-packaged candidates verified on 2026-05-24; 2026-05-26 refresh added MTP/speculative-decoding GGUF packages for runtime latency experiments. |
| 2 | Hermes | `NousResearch/Hermes-4-14B` / `NousResearch/Hermes-4.3-36B` | 14B / 36B | Inference yes, local LoRA tight or cloud-only | Baseline and calibration target | Hermes 4.3 36B is the newer public Hermes release; use 14B as the smaller first runtime target. |
| 3 | Gemma | `google/gemma-4-26B-A4B-it` | 26B total / 4B active | Inference yes, local fine-tune risky | Multimodal/agentic MoE target | Official HF model exists; GGUF/quant path must be validated for tool-call stability. |
| 4 | Qwen | `Qwen/Qwen3-4B-MLX-4bit` | 4B | Fine-tune yes | First training track | Local training is proven, but strict tool-call formatting needs better target data before scaling. |
| 5 | LFM | `LiquidAI/LFM2.5-1.2B-Instruct` / Thinking | 1.2B | Fine-tune yes | Low-latency helper model | Official card lists llama.cpp, MLX, vLLM support and Unsloth/TRL fine-tuning recipes. |
| 6 | LFM | `LiquidAI/LFM2.5-8B-A1B-GGUF` | 8B total / 1B active | Inference yes, local fine-tune defer | 8B LFM runtime baseline | Q4_K_M GGUF is SSD-acquired and runtime-proven through llama-completion; Hermes JSON prompt compliance failed. |
| 7 | LFM | `LiquidAI/LFM2-8B-A1B` | 8B-ish hybrid | Fine-tune possible, verify | Experimental LFM track | Local Ollama has LFM2 converter changes; validate before long runs. |
| 7 | Ministral | `mlx-community/Ministral-3-8B-Instruct-2512-4bit` | 8B | Fine-tune possible | Apache 2.0 8B baseline | Useful if Qwen/Gemma/LFM tool behavior regresses. |

## Tiny/Small Open-Weight Shortlist

These recent open-weight models from the tiny/small leaderboard are worth triage because they fit the 32GB class locally or through Colab burst compute.

| Family | Candidate | Fit | Suggested lane |
|---|---|---|---|
| Qwen | `Qwen3.5 0.8B`, `Qwen3.5 2B` | Easy local fit | Mac/MLX, Mac/Ollama, Colab burst runs |
| Liquid | `LFM2.5-1.2B-Instruct`, `LFM2 2.6B` | Easy local fit | Mac/MLX, Mac/Ollama, mem0 extraction/helper |
| Google | `Gemma 3n E4B Instruct` | Local/Colab fit | Mac/MLX or Colab, then GGUF if needed |
| Google | `Gemma 4 E2B` | Local/Colab fit | Official QAT q4_0 GGUF runtime-proven but empty-output blocked; try MLX/profile before scoring |
| Microsoft | `Phi-4 Mini` | Easy local fit | Mac/MLX, Mac/Ollama, safety/extractor experiments |
| IBM | `Granite 4.1 3B` | Easy local fit | Mac/MLX, Mac/Ollama, general helper lane |
| LG AI Research | `Exaone 4.0 1.2B` | Easy local fit | Mac/MLX, Mac/Ollama, lightweight helper lane |
| Cohere | `North Mini Code` | Local/Colab fit | Code-specialist lane, Colab-first if needed |
| OpenBMB | `MiniCPM5 1B MLX` | Easy local fit | Tiny helper/extraction candidate; MLX load proven, strict tool-call blocked |

These are triage candidates, not automatic fine-tune targets. The next step for each is a runtime proof and a role decision: Hermes helper, mem0 extractor, retrieval helper, or watchlist.

Verified HF ids behind this shortlist:

- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`
- `google/gemma-3n-E4B`
- `google/gemma-4-E2B`
- `microsoft/Phi-4-mini-instruct`
- `ibm-granite/granite-4.1-3b`
- `LGAI-EXAONE/EXAONE-4.0-1.2B`
- `CohereLabs/North-Mini-Code-1.0`
- `openbmb/MiniCPM5-1B`
- `openbmb/MiniCPM5-1B-MLX`
- `openbmb/MiniCPM5-1B-GGUF`
- `openbmb/MiniCPM5-1B-SFT`

## Research Frontier

| Family | Candidate | Status | How to Treat It |
|---|---|---|---|
| Qwen3-Next | `Qwen/Qwen3-Next-80B-A3B-Instruct`, Qwen3-Coder-Next | Real HF models/reports exist; local repo has Qwen3Next converter support | Runtime experiment first. Too large for first local fine-tune, but important for subquadratic/linear-attention roadmap. |
| Mamba-3 | State-space / selective SSM family | Current architecture family, not a drop-in Hermes model track yet | Watchlist. Add only after weights + Mac runtime + tokenizer are real. |
| RWKV-7 | `BlinkDL/rwkv7-g1`, `BlinkDL/rwkv-7-world` exact checkpoints | Real recurrent family with public checkpoints; no official 7B World checkpoint verified | Runtime experiment. Tool-calling chat quality must be tested. |
| BitNet b1.58 | Microsoft BitNet / QVAC BitLoRA ecosystem | Native runtime load/generation is locally proven; fine-tune path emerging | Research track. Prompt-compliance and non-interactive Hermes task smokes still block use. |
| Recursive wrappers | `mit-oasys/rlm-qwen3-8b-v0.1` and RLM-style harnesses | Real experimental checkpoint plus architecture/harness idea | Build only after a clear runtime harness and reproducible dataset objective exist. |

## Claims To Treat Carefully

These may be promising, but should not be promoted until verified with an actual model repo and Mac-capable runtime:

- `Kimi K2.6-Mini`
- `MiMo V2.5-Pro`
- `DeepSeek-V4-Flash`
- `SubQ 1M-Preview`
- `LFM 3 Preview`
- generic `RLM-Qwen3-8B` unless using the concrete `mit-oasys/rlm-qwen3-8b-v0.1` checkpoint and recording the harness

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

## Qwen3.6 / Hermes 4 Runtime Proof Track

`Qwen/Qwen3.6-35B-A3B` and `NousResearch/Hermes-4-14B` remain the next concrete runtime-proof targets. The 2026-05-22 no-download pass found no compatible local artifact or active endpoint, so both stay `needs-runtime-proof`.

Recorded result:

- No Qwen3.6 or Hermes 4 GGUF, MLX, safetensors, Ollama, or KTransformers-ready artifact was found on `/Volumes/PortableSSD`.
- Ollama (`127.0.0.1:11434`), MLX server (`127.0.0.1:8080`), and LM Studio (`127.0.0.1:1234`) endpoints were not listening.
- The only related local files were experimental config placeholders, not runnable model artifacts.
- Runtime evidence is recorded in `reports/runtime/qwen36-hermes4-runtime-proof/run-card.md`.

Recommended path:

1. Reuse only existing SSD-backed artifacts or documented local runtime paths.
2. Validate Qwen3.6 quantized inference through LM Studio or Ollama if a compatible artifact is already present.
3. Validate Hermes 4 through Ollama, LM Studio, or Transformers if the artifact is already available locally.
4. Record the exact command, endpoint, and smoke result under `/Volumes/PortableSSD`.
5. Treat missing artifacts as a tracking gap, not a download request.

## Unsupported Qwen3.7 Rumor Guardrail

As of 2026-05-24, Qwen3.7 should not be treated as a current public local model lane:

- No official Hugging Face open-weight repositories were verified under `Qwen/Qwen3.7-*`.
- Current Qwen3.7-Max/Plus reporting describes API/preview/proprietary availability, not redistributable local weights.
- Do not create MLX, Ollama, LM Studio, Azure fine-tune, GitHub publication, or Hugging Face publication tracks for Qwen3.7 until official weights, license, and runtime artifacts exist.

Promotion trigger: add a track only after an official Qwen model repo, quantized Mac runtime path, or clearly supported hosted API workflow is available and documented.

## Recurrent And Subquadratic Track

These are not just "long context" models. The point is lower memory growth and faster inference on long sequences.

Candidate families:

- **Qwen3.6 / Qwen3-Next:** hybrid Gated DeltaNet, MoE, and attention style architectures.
- **Mamba-3:** SSM/MIMO research direction with improved state tracking; treat as an architecture family until exact weights/runtime are verified.
- **RWKV-7:** recurrent/RNN-style language model family; use exact checkpoint names such as `BlinkDL/rwkv7-g1`.
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
| LFM2 8B-A1B / 24B-A2B | Check per build | Not needed | Local Ollama has converter work | Improving | Check | 8B-A1B is the safer LFM runtime target; 24B-A2B now has GGUF, ONNX, and MLX-bf16 package listings and should be treated as a runtime experiment before fine-tuning. |
| Mamba-3 | Research | No | No | No | No | Architecture watchlist until weights/runtime mature. |
| RWKV7 / rwkv-7-world | Limited | No | Check | Mixed | Mixed | Use exact public checkpoint sizes; tool-call quality must be tested. |
| BitNet | No | No | No | Native BitNet runtime proven; GGUF/endpoint path separate | No | Research track only; prompt-compliance failed. |

## Quantization And Runtime Notes

| Model | Current note | Status |
|---|---|---|
| `Qwen/Qwen3.6-35B-A3B` | Official HF weights are in Transformers format and the model card lists Transformers, vLLM, SGLang, and KTransformers compatibility. Keep LM Studio/Ollama/GGUF paths as `needs-runtime-proof` until a Mac run is recorded. | `needs-runtime-proof` |
| `NousResearch/Hermes-4-14B` | Official safetensors are published. Treat Transformers as the first known path and keep GGUF / FP8 / community quant paths as runtime candidates until this repo records a smoke result. | `needs-runtime-proof` |
| `google/gemma-4-26B-A4B-it` | Official image-text-to-text safetensors exist. Community GGUF and on-device quants may exist, but Mac runtime support remains `needs-runtime-proof` here. | `needs-runtime-proof` |
| `google/gemma-4-E2B-it-qat-q4_0-gguf` | Official QAT q4_0 text GGUF was acquired to SSD and load-proven through `llama-completion` on 2026-06-12. The bounded JSON prompt returned only end-of-text, with llama.cpp token/EOG warnings, so it needs a model-specific prompt profile or MLX proof before scoring. | `runtime-proofed; empty-output-blocked` |
| `Qwen/Qwen3-Next-80B-A3B-Instruct` | Official HF weights and a GGUF family are published. Use it as a runtime-experiment target only; it is not a 32GB fine-tune target. | `needs-runtime-proof` |
| `LiquidAI/LFM2-24B-A2B` | Live Hugging Face API refresh on 2026-05-24 found official base, GGUF, ONNX, and MLX-bf16 package listings plus a NexaAI GGUF. Treat as a specialist runtime experiment; do not make local fine-tune claims before endpoint and memory proofs. | `needs-runtime-proof` |
| `LiquidAI/LFM2.5-1.2B-Instruct` / `Thinking` | Official model card lists day-one support for llama.cpp, MLX, and vLLM. This is the safest local fine-tune lane in the frontier set. | `ready` |
| `LiquidAI/LFM2.5-8B-A1B-GGUF` | Official Q4_K_M GGUF was acquired to SSD and load/generation passed through `llama-completion` on 2026-06-12. The bounded JSON prompt produced non-compliant output, so it is a runtime baseline only. | `runtime-proofed; hermes-smoke-blocked` |
| `microsoft/bitnet-b1.58-2B-4T` | Native BitNet runtime load and 16-token generation passed on 2026-06-12 from the SSD-backed I2_S artifact with 1.32 GB max RSS. The bounded JSON prompt and `-cnv` chat-profile retry were non-compliant, so this is runtime evidence only. | `runtime-proofed; hermes-smoke-blocked` |
| `openbmb/MiniCPM5-1B-MLX` | Official MLX package acquired through the SSD-backed Hugging Face cache. A one-case direct MLX loglikelihood smoke passed on 2026-06-12, but the 3-case BFCL-style pilot scored 0.000 because outputs did not emit strict Hermes tool-call JSON. | `runtime-proofed; tool-call-blocked` |
| `Qwen/Qwen3.5-0.8B` / `Qwen/Qwen3.5-2B` | Both tiny MLX candidates are SSD-acquired and one-case loglikelihood proven. The raw BFCL-style role gate scored 0.000 for both; a simple `<tool_call>` wrapper retry for 0.8B also scored 0.000. Use only for prompt-repair/helper/extraction experiments. | `runtime-proofed; tool-call-blocked` |
| `CohereLabs/North-Mini-Code-1.0` / `unsloth/North-Mini-Code-1.0-GGUF` | The 18G Q4_K_M GGUF artifact was acquired on SSD, but Homebrew llama.cpp 9290 failed before generation with `unknown model architecture: 'cohere2moe'`. Do not retry the same runtime until `cohere2moe` support is present. | `runtime-blocked` |
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
