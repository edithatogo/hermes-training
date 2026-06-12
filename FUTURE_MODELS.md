# Bleeding-Edge Model Radar

This file is the model-selection radar for Hermes fine-tunes on a MacBook Pro M1 Max with 32GB RAM. Refresh it before starting a new track because model availability, MLX support, Ollama converter support, and quantized releases move quickly.

Latest scans:

- [Current release scan](./reports/model-radar/current-release-scan-20260524.md)
- [Qwen3.7/Qwen3.6/Hermes 4 availability check](./reports/model-radar/qwen37-qwen36-hermes4-check-20260524.md)
- [Harmonic-Hermes / Harmonic-9B scan](./reports/model-radar/harmonic-hermes-current-release-scan-20260612.md)
- [Nemotron 3 Nano 4B packaging scan](./reports/model-radar/nemotron3-nano-4b-packaging-current-release-scan-20260612.md)
- [Hermes-Qwen3.5 SFT v7 scan](./reports/model-radar/hermes-qwen35-sft-v7-current-release-scan-20260612.md)
- [Qwen3.6 35B 2-bit MLX scan](./reports/model-radar/qwen36-35b-2bit-mlx-current-release-scan-20260612.md)
- [Base-model release follow-up](./reports/model-radar/base-model-refresh-current-release-scan-20260612.md)
- [NVIDIA Nemotron follow-up](./reports/model-radar/nvidia-nemotron-follow-up-current-release-scan-20260612.md)

2026-06-12 refresh: the newest verified actionables are Hermes 4.3 36B / GGUF,
Harmonic-9B and Harmonic-Hermes-9B GGUF packaging, Gemma 4 12B it plus
Unsloth GGUF/qat packages, Gemma 4 31B-it, Gemma 4 31B base, and its NVFP4 packaging,
Qwen3.5-9B, Qwen3.5-27B, Qwen3.6-27B, Qwen3.6-35B 2-bit MLX packaging and its
FP8/GGUF/MLX packaging,
MiniCPM-o 4.5, MiniCPM-SALA, AgentCPM-Report, MiniCPM-V-4.6,
MiniCPM-V-4.6-GPTQ,
MiniCPM-V-4.6-Thinking, Nanbeige4.1-3B, Command A+, Step 3.7 Flash,
DeepSeek-V4-Flash and DeepSeek-V4-Flash-Base, Nemotron-Labs-Diffusion-14B,
Nemotron-Labs-Diffusion-VLM-8B, Nex-N2-mini, Nemotron 3.5 support models,
Nemotron 3 Ultra base/GenRM/speech checkpoints, and the larger Nemotron frontier set.
No verified official Qwen3.7 open-weight lane surfaced in the current Hugging
Face search. Keep Qwen3.6 MTP GGUF packages as runtime-latency experiments
behind the existing Qwen3.6 proof, and treat the new Gemma 4 12B/31B, Hermes
4.3, Harmonic-9B/Harmonic-Hermes-9B, Hermes-Qwen3.5 SFT v7 packs, Qwen3-4B 2507, Qwen3-Coder-Next, Qwen3-Embedding-4B, Qwen3-Reranker-4B,
Qwen3.5-9B, Qwen3.5-27B, Qwen3.6-27B, Qwen3.6-35B 2-bit MLX,
MiniCPM-o 4.5, MiniCPM-SALA,
AgentCPM-Report, MiniCPM-V-4.6, MiniCPM-V-4.6-Thinking, Nanbeige4.1-3B,
Command A+, Step 3.7 Flash, DeepSeek-V4-Flash, Nemotron-Labs-Diffusion,
Nex-N2-mini, Nemotron support entries, and Nemotron frontier entries as
runtime/helper, teacher, or specialist candidates rather than automatic
promotion targets.

No verified official Qwen3.7 open-weight local lane was found. Qwen3.7-Max/Plus
should be treated as API/preview/proprietary until official weights or a
supported hosted workflow are verified.

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
| 2 | Qwen | `Qwen/Qwen3.6-27B`, `unsloth/Qwen3.6-27B-GGUF`, `Qwen/Qwen3.6-27B-FP8` | 27B | Inference yes, local fine-tune risky | Dense small-model frontier target | Artificial Analysis now places Qwen3.6 27B among the highest-intelligence small open-source models. Use this as a dense comparison point before the larger MoE lane. |
| 3 | Hermes | `NousResearch/Hermes-4-14B` / `NousResearch/Hermes-4.3-36B` | 14B / 36B | Inference yes, local LoRA tight or cloud-only | Baseline and calibration target | Hermes 4.3 36B is the newer public Hermes release; use 14B as the smaller first runtime target. |
| 4 | Gemma | `google/gemma-4-26B-A4B-it` / `google/gemma-4-31B-it` | 26B / 31B | Inference yes, local fine-tune risky | Multimodal/agentic MoE target | Official HF models exist; 31B is the larger teacher baseline and both need runtime proof plus tool-call stability testing. |
| 5 | Gemma | `google/gemma-4-12B-it` / `google/gemma-4-12B`, `unsloth/gemma-4-12b-it-GGUF`, `unsloth/gemma-4-12B-it-qat-GGUF`, `batiai/gemma-4-12B-it-GGUF`, `DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF` | 12B | Runtime yes, fine-tune possible | Mid-size Mac/Colab candidate | Newer verified 12B Gemma 4 family plus fresh Unsloth and community GGUF/QAT packaging; useful before jumping to 26B/31B. |
| 6 | Qwen | `Qwen/Qwen3-4B-MLX-4bit` | 4B | Fine-tune yes | First training track | Local training is proven, but strict tool-call formatting needs better target data before scaling. |
| 7 | Qwen | `Qwen/Qwen3.5-27B` | 27B | Teacher yes, local fine-tune no | Dense mid-size teacher | Current HF repo plus community GGUF packaging make it a good comparison bridge between 9B and Qwen3.6-27B. |
| 8 | Cohere | `CohereLabs/command-a-plus-05-2026-w4a4` | 218B total / 25B active | Teacher yes, local fine-tune no | Agentic multimodal teacher | New open-source Command A+ release with a W4A4 path and vision support. |
| 9 | StepFun | `stepfun-ai/Step-3.7-Flash` | 198B total / ~11B active | Teacher yes, local fine-tune no | Agentic and reasoning-heavy teacher | Large sparse MoE vision-language model with tool/workflow benchmark claims. |
| 10 | Nex-AGI | `nex-agi/Nex-N2-mini` | 9B | Runtime yes, fine-tune maybe later | Small agentic runtime candidate | Community MLX conversions already exist, so it is a plausible Mac or Colab runtime path. |
| 11 | OpenBMB | `openbmb/MiniCPM-o-4_5` | 9B | Runtime yes, fine-tune maybe later | Multimodal helper / runtime lane | Official audio/vision MiniCPM release with visible GGUF and community MLX packaging. Good candidate for local helper workflows on Mac or Colab. |
| 12 | OpenBMB | `openbmb/MiniCPM-V-4.6` | 9B | Runtime yes, fine-tune maybe later | Multimodal helper / runtime lane | Edge-deployment-friendly VLM for OCR and document parsing. |
| 13 | OpenBMB | `openbmb/MiniCPM-V-4.6-Thinking` | 9B | Runtime yes, fine-tune maybe later | Multimodal helper / runtime lane | Thinking variant adds a multimodal reasoning comparison point for helper workflows. |
| 14 | OpenBMB | `openbmb/AgentCPM-Report` | 8B | Runtime yes, fine-tune maybe later | Deep research agent | Open-ended deep research agent with long-horizon comparison value for Hermes workflows. |
| 15 | Nanbeige | `Nanbeige/Nanbeige4.1-3B` | 3B | Runtime yes, fine-tune maybe later | Tiny reasoning/helper lane | New tiny-model leaderboard candidate with plausible helper/extractor value on 32GB or Colab. |
| 16 | NVIDIA | `nvidia/Nemotron-Labs-Diffusion-14B` | 14B | Runtime yes, fine-tune no | Speed/reasoning research lane | Tri-mode AR/diffusion/self-speculation language model. Use as a decoding-speed reference, not a default Hermes target. |
| 17 | NVIDIA | `nvidia/Nemotron-Labs-Diffusion-VLM-8B` | 8B | Runtime yes, fine-tune no | Multimodal speed/reasoning research lane | Diffusion VLM from the same family; useful for modality and parallel-decoding experiments. |
| 18 | NVIDIA | `nvidia/Nemotron-3.5-Content-Safety` | safety classifier | Runtime yes, fine-tune no | Specialist support lane | Safety moderator with custom-policy enforcement; keep out of Hermes text-generation lanes. |
| 19 | NVIDIA | `nvidia/nemotron-3.5-asr-streaming-0.6b` | 0.6B | Runtime yes, fine-tune no | Speech / ASR support lane | Streaming ASR model for low-latency transcription and multimodal pipelines. |
| 20 | NVIDIA | `nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16` | 30B total / 3B active | Teacher yes, local fine-tune no | Multimodal reasoning teacher | Expands the upper-end comparison set for Hermes-style work. |
| 21 | NVIDIA | `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4` / `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16` | 120B / 550B total | Teacher yes, local fine-tune no | Large collaborative-agent teacher | High-end reasoning/chat models with NVFP4 and BF16 packaging. Keep them in the cloud-teacher lane only. |
| 22 | NVIDIA | `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16` | 30B total / 3B active | Teacher yes, local fine-tune no | Reasoning/chat teacher | Smaller Nemotron reasoning model with explicit reasoning-trace behavior. |
| 23 | NVIDIA | `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16`, `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`, `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF`, `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | 4B | Runtime yes, fine-tune maybe later | Small helper/runtime lane | Official 4B base plus fresh GGUF and MLX packaging for Mac-local use. |
| 24 | Hermes | `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`, `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`, `mkadrlik/hermes-Qwen3.5-2B-SFT-v7`, `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`, `mkadrlik/Hermes-27B-SFT-v7` | 0.8B-27B | Runtime yes, fine-tune maybe later | Hermes-Qwen3.5 local/runtime lane | Fresh Hermes-style GGUF packs directly on the Qwen3.5 family; treat as the new local comparison set. |
| 25 | NVIDIA | `nvidia/Qwen3-Nemotron-235B-A22B-GenRM-2603` | 235B total / 22B active | Teacher/evaluator only | Reward model / evaluator lane | Used in Nemotron training; keep it out of the chat lane. |
| 26 | DeepSeek | `deepseek-ai/DeepSeek-V4-Flash` / `deepseek-ai/DeepSeek-V4-Flash-Base` | 284B total / 13B active | Teacher yes, local fine-tune no | Long-context cloud teacher | Frontier long-context MoE and its base variant; use as benchmark reference, not a 32GB local training target. |
| 27 | LFM | `LiquidAI/LFM2.5-1.2B-Instruct` / Thinking | 1.2B | Fine-tune yes | Low-latency helper model | Official card lists llama.cpp, MLX, vLLM support and Unsloth/TRL fine-tuning recipes. |
| 28 | LFM | `LiquidAI/LFM2.5-8B-A1B-GGUF` | 8B total / 1B active | Inference yes, local fine-tune defer | 8B LFM runtime baseline | Q4_K_M GGUF is SSD-acquired and runtime-proven through llama-completion; Hermes JSON prompt compliance failed. |
| 29 | LFM | `LiquidAI/LFM2-8B-A1B` | 8B-ish hybrid | Fine-tune possible, verify | Experimental LFM track | Local Ollama has LFM2 converter changes; validate before long runs. |
| 30 | Ministral | `mlx-community/Ministral-3-8B-Instruct-2512-4bit` | 8B | Fine-tune possible | Apache 2.0 8B baseline | Useful if Qwen/Gemma/LFM tool behavior regresses. |
| 31 | Qwen | `Qwen/Qwen3-4B-Instruct-2507`, `Qwen/Qwen3-4B-Thinking-2507` | 4B | Runtime yes, fine-tune possible | Current Qwen refresh | Official 2507 releases with 256K context and stronger thinking/non-thinking behavior. Good hosted or burst-compute comparison points. |
| 32 | Qwen | `Qwen/Qwen3-Coder-Next-GGUF` | 80B total / 3B active | Runtime yes, local fine-tune no | Coding-agent runtime lane | Official GGUF tree exposes Q4_K_M and Hermes Agent setup, making it the strongest current Qwen specialist runtime lane for Hermes workflows. |
| 33 | Qwen | `Qwen/Qwen3-Embedding-0.6B`, `Qwen/Qwen3-Reranker-0.6B` | 0.6B | Retrieval | Hermes memory/RAG fit | Official small Qwen retrieval models. Better 32GB-class fit than the 4B pair; the reranker already has local benchmark evidence. |
| 34 | Qwen | `Qwen/Qwen3-Embedding-4B`, `Qwen/Qwen3-Reranker-4B` | embedding / reranker | Retrieval | Retrieval support lane | Official Qwen retrieval models. Use for Hermes memory and RAG, not chat SFT. |

## Tiny/Small Open-Weight Shortlist

These recent open-weight models from the tiny/small leaderboard are worth triage because they fit the 32GB class locally or through Colab burst compute.

| Family | Candidate | Fit | Suggested lane |
|---|---|---|---|
| Qwen | `Qwen3.5 0.8B`, `Qwen3.5 2B` | Easy local fit | Mac/MLX, Mac/Ollama, Colab burst runs |
| Qwen | `Qwen3-4B-Instruct-2507`, `Qwen3-4B-Thinking-2507` | Local/Colab fit | Current Qwen refresh for hosted or burst GPU runs; no Mac-native packaging verified in this refresh |
| Qwen | `Qwen3-Coder-Next-GGUF` | Local runtime fit | Hermes Agent-compatible coding-agent baseline, best Qwen specialist runtime lane |
| Qwen | `Qwen3-Embedding-0.6B`, `Qwen3-Reranker-0.6B` | Local fit | Small retrieval pair for Hermes memory/RAG; lighter than the 4B pair |
| Qwen | `Qwen3-Embedding-4B`, `Qwen3-Reranker-4B` | Local/Colab fit | Retrieval lane for Hermes memory and RAG; compare against BGE-M3 and Jina embeddings |
| Qwen | `Qwen3.5 27B` | Dense teacher fit | Mac GGUF/MLX packaging or Colab burst runs; dense mid-size comparison point |
| Qwen | `Qwen3.6 27B` | Dense small-model fit | Mac GGUF/MLX packaging or Colab burst runs; dense frontier comparison point |
| Qwen | `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming` | Local fit | Fresh 2-bit MLX local-runtime candidate with tool-calling/agentic tags |
| Liquid | `LFM2.5-1.2B-Instruct`, `LFM2 2.6B` | Easy local fit | Mac/MLX, Mac/Ollama, mem0 extraction/helper |
| Google | `Gemma 3n E4B Instruct` | Local/Colab fit | Mac/MLX or Colab, then GGUF if needed |
| Google | `Gemma 4 E4B MLX` | Local/Colab fit | MLX load proven but Hermes no-extra-text strict gate remains 0/3; score-only native normalizer rescues 1/3 |
| Google | `Gemma 4 E2B`, `Gemma 4 E2B QAT Mobile` | Local/Colab fit | Official QAT q4_0 GGUF runtime-proven but empty-output blocked; the mobile package is a fresh lightweight comparison point |
| Google | `Gemma 4 12B` | Local/Colab fit | Newer mid-size Gemma 4 lane; verify runtime and memory behavior before promotion |
| Google/Unsloth | `Gemma 4 12B GGUF`, `Gemma 4 12B QAT GGUF` | Local fit | Fresh packaging lanes for the 12B Gemma 4 family; compare against the native Transformers release |
| Community | `batiai/gemma-4-12B-it-GGUF`, `DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF` | Local fit | New community GGUF packagers with explicit local-runtime instructions |
| Microsoft | `Phi-4 Mini` | Easy local fit | Mac/MLX, Mac/Ollama, safety/extractor experiments |
| IBM | `Granite 4.1 3B` | Easy local fit | Mac/MLX, Mac/Ollama, helper/extraction lane; raw strict BFCL pilot 1/3, native-normalized strict pilot 2/3 |
| Qwen | `Qwen3.5 9B` | Local/Colab fit | Mid-size helper/tool candidate, stronger than the tiny 0.8B/2B lanes if it proves stable |
| Hermes | `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`, `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`, `mkadrlik/hermes-Qwen3.5-2B-SFT-v7`, `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | Local fit | Fresh Hermes-style Qwen3.5 GGUF packs, with 9B as the primary new comparison lane |
| NVIDIA | `NVIDIA-Nemotron-3-Nano-4B-BF16`, `NVIDIA-Nemotron-3-Nano-4B-GGUF`, `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF`, `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | Local/Colab fit | Small helper/runtime lane with official base plus GGUF and MLX packaging |
| Hermes | `Harmonic-9B`, `Harmonic-Hermes-9B-GGUF`, `mradermacher/Harmonic-Hermes-9B-i1-GGUF` | Local fit | Stage 2 agentic fine-tune on Harmonic-9B; good Hermes-style Mac runtime comparison lane |
| Cohere | `Command A+ 05 2026` | Teacher / cloud fit | Agentic multimodal teacher candidate, not a local Mac fine-tune target |
| StepFun | `Step 3.7 Flash` | Teacher / cloud fit | Large sparse-MoE teacher with strong agentic benchmark claims |
| Nex-AGI | `Nex-N2-mini` | Local/Colab fit | Small agentic runtime candidate with MLX community conversions already published |
| OpenBMB | `MiniCPM-o 4.5` | Local/Colab fit | Multimodal voice/vision helper with visible GGUF and MLX packaging, useful for non-text agent workflows |
| OpenBMB | `MiniCPM-V-4.6` | Local/Colab fit | Edge-deployment-friendly VLM for OCR, PDF parsing, and multimodal helper workflows |
| OpenBMB | `MiniCPM-V-4.6-Thinking` | Local/Colab fit | Multimodal helper workflows with a reasoning-oriented comparison point |
| OpenBMB | `MiniCPM-V-4.6-BNB` | Local/Colab fit | Lightweight multimodal packaging comparison point |
| OpenBMB | `MiniCPM-SALA` | Research/runtime | Long-context hybrid sparse/linear-attention model for context-heavy helper work |
| OpenBMB | `AgentCPM-Report` | Research/runtime | Deep-research agent lane for long-horizon Hermes comparison and orchestration experiments |
| Nanbeige | `Nanbeige4.1-3B` | Local/Colab fit | Tiny reasoning/helper lane with plausible extraction value |
| NVIDIA | `Nemotron-Labs-Diffusion-14B` | Research/runtime | Tri-mode AR/diffusion/self-speculation lane for speed and decoding experiments |
| NVIDIA | `Nemotron-Labs-Diffusion-VLM-8B` | Research/runtime | Multimodal diffusion lane for parallel-decoding and modality experiments |
| NVIDIA | `Nemotron 3.5 Content Safety` | Specialist support | Safety moderator for policy enforcement and moderation |
| NVIDIA | `Nemotron 3.5 ASR Streaming 0.6B` | Specialist support | Low-latency streaming speech-to-text lane, not a Hermes text model |
| NVIDIA | `Nemotron 3 Nano Omni 30B-A3B Reasoning` | Teacher / cloud fit | Multimodal reasoning teacher with a stronger agentic comparison baseline |
| NVIDIA | `NVIDIA Nemotron 3 Super 120B-A12B` | Teacher / cloud fit | Large collaborative-agent teacher, not a local fine-tune target |
| NVIDIA | `NVIDIA Nemotron 3 Nano 30B-A3B` | Teacher / cloud fit | Smaller reasoning/chat teacher with explicit reasoning traces |
| NVIDIA | `Qwen3-Nemotron 235B-A22B GenRM` | Teacher / evaluator | Reward model lane for evaluation and RLHF-style comparisons |
| LG AI Research | `Exaone 4.0 1.2B` | Easy local fit | GGUF runtime-proven under 1GB RSS; MLX blocked by current config bug; Hermes JSON blocked |
| Cohere | `North Mini Code` | Local/Colab fit | Code-specialist lane, Colab-first if needed |
| OpenBMB | `MiniCPM5 1B MLX` | Easy local fit | Tiny helper/extraction candidate; MLX load proven, strict tool-call blocked |

These are triage candidates, not automatic fine-tune targets. The next step for each is a runtime proof and a role decision: Hermes helper, mem0 extractor, retrieval helper, or watchlist.

Verified HF ids behind this shortlist:

- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`
- `Qwen/Qwen3.5-9B`
- `Qwen/Qwen3.5-27B`
- `Qwen/Qwen3-4B-Instruct-2507`
- `Qwen/Qwen3-4B-Thinking-2507`
- `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`
- `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`
- `mkadrlik/hermes-Qwen3.5-2B-SFT-v7`
- `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`
- `mkadrlik/Hermes-27B-SFT-v7`
- `Qwen/Qwen3-Coder-Next`
- `Qwen/Qwen3-Coder-Next-GGUF`
- `Qwen/Qwen3-Embedding-0.6B`
- `Qwen/Qwen3-Reranker-0.6B`
- `Qwen/Qwen3-Embedding-4B`
- `Qwen/Qwen3-Reranker-4B`
- `DJLougen/Harmonic-9B`
- `DJLougen/Harmonic-Hermes-9B-GGUF`
- `mradermacher/Harmonic-Hermes-9B-i1-GGUF`
- `google/gemma-3n-E4B`
- `google/gemma-4-E2B`
- `google/gemma-4-E2B-it-qat-mobile-transformers`
- `google/gemma-4-12B`
- `google/gemma-4-12B-it`
- `unsloth/gemma-4-12b-it-GGUF`
- `unsloth/gemma-4-12B-it-qat-GGUF`
- `batiai/gemma-4-12B-it-GGUF`
- `DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF`
- `microsoft/Phi-4-mini-instruct`
- `ibm-granite/granite-4.1-3b`
- `LGAI-EXAONE/EXAONE-4.0-1.2B`
- `CohereLabs/North-Mini-Code-1.0`
- `openbmb/MiniCPM5-1B`
- `openbmb/MiniCPM5-1B-MLX`
- `openbmb/MiniCPM5-1B-GGUF`
- `openbmb/MiniCPM5-1B-SFT`
- `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16`
- `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`
- `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF`
- `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit`
- `openbmb/MiniCPM-V-4.6-Thinking`
- `openbmb/MiniCPM-V-4.6-BNB`
- `Nanbeige/Nanbeige4.1-3B`

## Research Frontier

| Family | Candidate | Status | How to Treat It |
|---|---|---|---|
| Qwen3-Next | `Qwen/Qwen3-Next-80B-A3B-Instruct`, Qwen3-Coder-Next | Real HF models/reports exist; local repo has Qwen3Next converter support | Runtime experiment first. Too large for first local fine-tune, but important for subquadratic/linear-attention roadmap. |
| Mamba-3 | State-space / selective SSM family | Current architecture family, not a drop-in Hermes model track yet | Watchlist. Add only after weights + Mac runtime + tokenizer are real. |
| RWKV-7 | `BlinkDL/rwkv7-g1`, `BlinkDL/rwkv-7-world` exact checkpoints | Real recurrent family with public checkpoints; no official 7B World checkpoint verified | Runtime experiment. Tool-calling chat quality must be tested. |
| DiffusionGemma | `google/diffusiongemma-26B-A4B-it`, `nvidia/diffusiongemma-26B-A4B-it-NVFP4`, `mlx-community/diffusiongemma-26B-A4B-it-mxfp4` | Fresh official diffusion-family release plus fresh packaging variants | Research/runtime. Useful for multimodal diffusion and decoding experiments, not a Hermes adapter target. |
| BitNet b1.58 | Microsoft BitNet / QVAC BitLoRA ecosystem | Native runtime load/generation is locally proven; fine-tune path emerging | Research track. Prompt-compliance and non-interactive Hermes task smokes still block use. |
| Recursive wrappers | `mit-oasys/rlm-qwen3-8b-v0.1` and RLM-style harnesses | Real experimental checkpoint plus architecture/harness idea | Build only after a clear runtime harness and reproducible dataset objective exist. |

## Claims To Treat Carefully

These may be promising, but should not be promoted until verified with an actual model repo and Mac-capable runtime:

- `Kimi K2.6-Mini`
- `MiMo V2.5-Pro`
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
| `Qwen/Qwen3.6-27B` | Official HF weights are published, and current searches surface FP8, GGUF, and MLX packaging. Treat as the denser Qwen3.6 comparison point rather than a first local fine-tune target. | `needs-runtime-proof` |
| `NousResearch/Hermes-4-14B` | Official safetensors are published. Treat Transformers as the first known path and keep GGUF / FP8 / community quant paths as runtime candidates until this repo records a smoke result. | `needs-runtime-proof` |
| `google/gemma-4-26B-A4B-it` | Official image-text-to-text safetensors exist. Community GGUF and on-device quants may exist, but Mac runtime support remains `needs-runtime-proof` here. | `needs-runtime-proof` |
| `google/gemma-4-E2B-it-qat-q4_0-gguf` | Official QAT q4_0 text GGUF was acquired to SSD and load-proven through `llama-completion` on 2026-06-12. The bounded JSON prompt returned only end-of-text, with llama.cpp token/EOG warnings, so it needs a model-specific prompt profile or MLX proof before scoring. | `runtime-proofed; empty-output-blocked` |
| `mlx-community/gemma-4-E4B-it-qat-4bit` | MLX package was SSD-acquired and direct MLX scoring passed on 2026-06-12. One-case greedy match was 0.000 and the raw BFCL-style pilot scored 0.000 due to Gemma thought/tool fragments. A score-only Gemma-native normalizer and permissive prompt profile each reached 1/3, but no-extra-text Hermes strict scoring stayed 0/3. | `runtime-proofed; tool-call-blocked` |
| `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF` / `mlx-community/exaone-4.0-1.2b-4bit` | Official Q4_K_M GGUF was acquired to SSD and load/generation passed through `llama-completion` on 2026-06-12 with under 1GB max RSS, but output repeated braces instead of JSON. The MLX 4-bit package is acquired but blocked by a Transformers EXAONE4 config `ZeroDivisionError`. | `gguf-runtime-proofed; mlx-blocked; hermes-smoke-blocked` |
| `Qwen/Qwen3-Next-80B-A3B-Instruct` | Official HF weights and a GGUF family are published. Use it as a runtime-experiment target only; it is not a 32GB fine-tune target. | `needs-runtime-proof` |
| `LiquidAI/LFM2-24B-A2B` | Live Hugging Face API refresh on 2026-05-24 found official base, GGUF, ONNX, and MLX-bf16 package listings plus a NexaAI GGUF. Treat as a specialist runtime experiment; do not make local fine-tune claims before endpoint and memory proofs. | `needs-runtime-proof` |
| `LiquidAI/LFM2.5-1.2B-Instruct` / `Thinking` | Official model card lists day-one support for llama.cpp, MLX, and vLLM. This is the safest local fine-tune lane in the frontier set. | `ready` |
| `LiquidAI/LFM2.5-8B-A1B-GGUF` | Official Q4_K_M GGUF was acquired to SSD and load/generation passed through `llama-completion` on 2026-06-12. The bounded JSON prompt produced non-compliant output, so it is a runtime baseline only. | `runtime-proofed; hermes-smoke-blocked` |
| `microsoft/bitnet-b1.58-2B-4T` | Native BitNet runtime load and 16-token generation passed on 2026-06-12 from the SSD-backed I2_S artifact with 1.32 GB max RSS. The bounded JSON prompt and `-cnv` chat-profile retry were non-compliant, so this is runtime evidence only. | `runtime-proofed; hermes-smoke-blocked` |
| `openbmb/MiniCPM5-1B-MLX` | Official MLX package acquired through the SSD-backed Hugging Face cache. A one-case direct MLX loglikelihood smoke passed on 2026-06-12, but the 3-case BFCL-style pilot scored 0.000 because outputs did not emit strict Hermes tool-call JSON. | `runtime-proofed; tool-call-blocked` |
| `Qwen/Qwen3.5-0.8B` / `Qwen/Qwen3.5-2B` | Both tiny MLX candidates are SSD-acquired and one-case loglikelihood proven. The raw BFCL-style role gate scored 0.000 for both; a simple `<tool_call>` wrapper retry for 0.8B also scored 0.000. Use only for prompt-repair/helper/extraction experiments. | `runtime-proofed; tool-call-blocked` |
| `google/gemma-4-31B-it` | Official 31B Gemma 4 instruction model with a visible community GGUF path. Treat as a larger teacher baseline and packaging comparison point, not a 32GB Mac fine-tune target. | `needs-runtime-proof` |
| `nvidia/Gemma-4-31B-IT-NVFP4` | NVIDIA-published quantized packaging for Gemma 4 31B. Keep as a cloud packaging comparison only. | `needs-runtime-proof` |
| `openbmb/MiniCPM-o-4_5` / `openbmb/MiniCPM-o-4_5-gguf` | Official multimodal MiniCPM release with visible GGUF packaging and community MLX coverage. Use for helper and non-text agent workflows after runtime proof. | `needs-runtime-proof` |
| `openbmb/MiniCPM-SALA` | Hybrid sparse/linear-attention long-context model. Treat as research/runtime only until a concrete helper workflow and runtime proof exist. | `needs-runtime-proof` |
| `openbmb/AgentCPM-Report` / `openbmb/AgentCPM-Report-GGUF` | Deep research agent and GGUF packaging. Keep in the research/runtime lane only. | `needs-runtime-proof` |
| `openbmb/MiniCPM-V-4.6` / `openbmb/MiniCPM-V-4.6-gguf` | Edge-deployment-friendly VLM with visible GGUF packaging. Use as a multimodal helper/runtime lane. | `needs-runtime-proof` |
| `nvidia/Nemotron-Labs-Diffusion-14B` | Tri-mode AR/diffusion/self-speculation text model. Use as a speed/reasoning reference only. | `needs-runtime-proof` |
| `nvidia/Nemotron-Labs-Diffusion-VLM-8B` | Multimodal diffusion VLM from the same family. Use for modality and parallel-decoding experiments. | `needs-runtime-proof` |
| `deepseek-ai/DeepSeek-V4-Flash` | Official preview MoE long-context model. Keep as cloud-teacher/reference only until a real endpoint or local runtime proof exists. | `needs-runtime-proof` |
| `deepseek-ai/DeepSeek-V4-Flash-Base` | Base variant of the DeepSeek V4 Flash line. Track only as a packaging/runtime reference. | `needs-runtime-proof` |
| `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16` | Frontier-scale Nemotron 3 Ultra model with explicit reasoning traces. Cloud-teacher only. | `needs-runtime-proof` |
| `CohereLabs/North-Mini-Code-1.0` / `unsloth/North-Mini-Code-1.0-GGUF` | The 18G Q4_K_M GGUF artifact was acquired on SSD, but Homebrew llama.cpp 9290 failed before generation with `unknown model architecture: 'cohere2moe'`. Do not retry the same runtime until `cohere2moe` support is present. | `runtime-blocked` |
| `BAAI/bge-m3` | Official retrieval model with FlagEmbedding / sentence-transformers usage. Treat as retrieval-only, not a chat quantization target. | `ready` |
| `jinaai/jina-embeddings-v4` | Official multimodal retrieval model. Use Transformers or sentence-transformers and keep it in the retrieval lane. | `needs-runtime-proof` |
| `LiquidAI/LFM2-ColBERT-350M` | Official late-interaction retriever with PyLate / sentence-transformers usage. Retrieval and reranking only; do not treat it as a generation model. | `needs-runtime-proof` |

## Sources Checked

- Qwen/Qwen3.6-35B-A3B and Qwen/Qwen3.6-27B model cards.
- Qwen/Qwen3-4B-Instruct-2507, Qwen/Qwen3-4B-Thinking-2507, Qwen/Qwen3-Coder-Next, and Qwen/Qwen3-Coder-Next-GGUF model cards.
- NousResearch/Hermes-4-14B Hugging Face repo and Hermes 4 technical report.
- google/gemma-4-26B-A4B-it, google/gemma-4-31B-it, and LM Studio / NVIDIA quantized Gemma 4 model cards.
- Google Gemma 4 collection and Unsloth Gemma 4 collection.
- openbmb/MiniCPM-o-4_5 and MiniCPM-o-4_5-gguf model cards.
- DeepSeek-V4-Flash model card and NVIDIA Nemotron 3 Ultra model cards.
- LiquidAI/LFM2.5 model card, Liquid LEAP fine-tuning docs, and the BitNet / QVAC BitLoRA fine-tuning blog.
- KTransformers Qwen SFT docs.
- Mamba-3 paper.
- Local Ollama repo converter/runtime support for LFM2, Qwen3Next, Gemma4, safetensors, and MLX runner.
