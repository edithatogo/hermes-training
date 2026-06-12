# All-Candidate Benchmark Coverage - 2026-06-12

Run ID: `all-candidate-benchmark-coverage-20260612`
Created: `2026-06-12T15:06:42.414840+00:00`

## Direct Answer

No: the repo has benchmark evidence for the active Hermes and mem0 lanes, but not promotion-grade benchmark coverage for every candidate in the registries.

The three-case smokes are appropriate only as liveness and regression checks. They are not sufficiently discriminating when multiple candidates tie. Promotion requires the role-specific expanded suites recorded below.

## Runtime-Proof Queue

The executable follow-up queue is generated at [`runtime-proof-action-queue-20260613.md`](./runtime-proof-action-queue-20260613.md). It separates Mac runtime proofs, prompt-profile repairs, support-model proofs, cloud teacher proofs, specialist runtime proofs, and watchlist entries so the remaining blocked Hermes candidates can be worked in bounded batches.

## Counts

| Project | Coverage state | Count |
|---|---|---:|
| hermes | `benchmarked-not-promoted` | 5 |
| hermes | `blocked` | 143 |
| hermes | `evidence-present-needs-review` | 2 |
| hermes | `smoke-or-pilot-only` | 5 |
| mem0 | `benchmarked-not-necessarily-promoted` | 11 |
| mem0 | `benchmarked-not-promoted` | 1 |
| mem0 | `blocked` | 3 |
| mem0 | `smoke-or-pilot-only` | 1 |

## Benchmark Policy

| Lane | Minimum useful gate | Promotion-grade gate |
|---|---|---|
| Hermes chat/tool-call | runtime smoke plus held-out strict tool-call | held-out strict, mirrored strict, local pilots, selected official/lm-eval coverage, and failure analysis |
| Hermes teacher/frontier | runtime proof plus strict tool-call sample | cloud/local repeatable endpoint, strict tool-call comparison, teacher-eval usefulness, cost/capacity record |
| mem0 embedder | direct retrieval smoke | expanded/adversarial retrieval, collection migration proof, rollback proof, latency and memory footprint |
| mem0 reranker | fixed rerank smoke | expanded replay, live multi-result fixture, cold/warm latency, vector fallback |
| mem0 retriever | service/index smoke | separate index lifecycle, expanded replay, rollback/default isolation proof |
| mem0 extractor | JSON extraction smoke | expanded durable extraction, forbidden-hit and empty-case gates, latency |

## Blocked Reasons

| Project | Candidate | State | Blocked reason | Evidence |
|---|---|---|---|---|
| hermes | `Qwen/Qwen3.6-35B-A3B` | `blocked` | blocked by strict Hermes tool-call formatting failure | `reports/runtime/qwen36-35b-a3b-q4-llamacpp-proof-20260525.md` |
| hermes | `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `deepsweet/Qwen3.6-35B-A3B-MLX-oQ4` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `qwen3.7-open-weights-watch` | `blocked` | blocked because open local weights or a supported public runtime are not verified |  |
| hermes | `mlx-community/Qwen3-VL-32B-Instruct-4bit` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `NousResearch/Hermes-4.3-36B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `NousResearch/Hermes-4.3-36B-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `DJLougen/Harmonic-9B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `DJLougen/Harmonic-Hermes-9B-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mradermacher/Harmonic-Hermes-9B-i1-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mkadrlik/hermes-Qwen3.5-2B-SFT-v7` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mkadrlik/Hermes-27B-SFT-v7` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-4-12B-it` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-4-12B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `unsloth/gemma-4-12b-it-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `unsloth/gemma-4-12B-it-qat-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `batiai/gemma-4-12B-it-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-4-26B-A4B-it` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-4-31B-it` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-4-31B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-4-E2B-it-qat-q4_0-gguf` | `blocked` | blocked by strict Hermes tool-call formatting failure | `reports/benchmark/local-pilots/gemma4-e2b-q4-llamacpp-strict-bfcl-pilot-20260613.md`<br>`reports/model-radar/gemma4-e2b-it-packaging-refresh-current-release-scan-20260612.md`<br>`reports/runtime/gemma4-e2b-q4-llamacpp-smoke-20260612.md` |
| hermes | `google/gemma-4-E2B-it` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-4-E2B-it-qat-mobile-transformers` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `litert-community/gemma-4-E2B-it-litert-lm` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mlx-community/gemma-4-e2b-it-4bit` | `blocked` | blocked by current local runtime support | `reports/runtime/gemma4-e2b-mlx-4bit-load-failure-20260613.md` |
| hermes | `mlx-community/gemma-4-E4B-it-qat-4bit` | `blocked` | blocked by strict Hermes tool-call formatting failure | `reports/benchmark/local-pilots/gemma4-e4b-native-normalized-pilot-20260612.md`<br>`reports/benchmark/local-pilots/gemma4-e4b-strict-profile-no-extra-pilot-20260612.md`<br>`reports/benchmark/mlx-loglikelihood/gemma4-e4b-mlx-loglikelihood-smoke-20260612.md` |
| hermes | `google/gemma-4-E4B-it-qat-mobile-transformers` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `unsloth/gemma-4-26B-A4B-it-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `lmstudio-community/gemma-4-31B-it-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `unsloth/gemma-4-31B-it-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `ggml-org/gemma-4-31B-it-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `bartowski/google_gemma-4-31B-it-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-4-31B-it-qat-q4_0-gguf` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/Gemma-4-31B-IT-NVFP4` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/Gemma-4-26B-A4B-NVFP4` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3.5-0.8B` | `blocked` | blocked by empty/no-content generation under the strict prompt | `reports/benchmark/local-pilots/qwen3-5-0-8b-local-bfcl-pilot-20260613.md` |
| hermes | `Qwen/Qwen3.5-2B` | `blocked` | blocked by empty/no-content generation under the strict prompt | `reports/benchmark/local-pilots/qwen3-5-2b-local-bfcl-pilot-20260613.md` |
| hermes | `Qwen/Qwen3.5-9B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-4B-Instruct-2507` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-4B-Thinking-2507` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3.5-27B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `CohereLabs/command-a-plus-05-2026-w4a4` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `stepfun-ai/Step-3.7-Flash` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nex-agi/Nex-N2-mini` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-Coder-Next-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-Coder-Next` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/Nemotron-3.5-Content-Safety` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/nemotron-3.5-asr-streaming-0.6b` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/Qwen3-Nemotron-235B-A22B-GenRM-2603` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-Base-BF16` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-GenRM` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/nemotron-speech-streaming-en-0.6b` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-ASR-1.7B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-Omni-30B-A3B-Instruct` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-Omni-30B-A3B-Captioner` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `microsoft/Phi-4-multimodal-instruct` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `CohereLabs/cohere-transcribe-03-2026` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/parakeet-tdt-0.6b-v3` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/instant-nurec` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/omni-dreams-models` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/Nemotron-Labs-Diffusion-14B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/Nemotron-Labs-Diffusion-VLM-8B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/diffusiongemma-26B-A4B-it` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/diffusiongemma-26B-A4B-it-NVFP4` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mlx-community/diffusiongemma-26B-A4B-it-mxfp4` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `deepseek-ai/DeepSeek-V4-Flash` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `deepseek-ai/DeepSeek-V4-Flash-Base` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-3n-E4B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `google/gemma-4-E2B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `microsoft/Phi-4-mini-instruct` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `ibm-granite/granite-4.1-3b` | `blocked` | blocked by strict Hermes tool-call formatting failure |  |
| hermes | `LGAI-EXAONE/EXAONE-4.0-1.2B` | `blocked` | blocked by strict Hermes tool-call formatting failure | `reports/benchmark/local-pilots/exaone4-12b-q4km-llamacpp-strict-bfcl-pilot-20260613.md`<br>`reports/runtime/exaone4-12b-q4km-llamacpp-smoke-20260612.md` |
| hermes | `openbmb/MiniCPM5-1B-MLX` | `blocked` | blocked by empty/no-content generation under the strict prompt | `reports/benchmark/local-pilots/minicpm5-1b-mlx-local-bfcl-pilot-20260612.md`<br>`reports/benchmark/local-pilots/minicpm5-1b-mlx-strict-bfcl-pilot-20260613.md`<br>`reports/benchmark/mlx-loglikelihood/minicpm5-1b-mlx-loglikelihood-smoke-20260612.md` |
| hermes | `openbmb/MiniCPM5-1B-GGUF` | `blocked` | blocked by strict Hermes tool-call formatting failure | `reports/benchmark/local-pilots/minicpm5-1b-q4km-llamacpp-strict-bfcl-pilot-20260613.md` |
| hermes | `Nanbeige/Nanbeige4.1-3B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Mungert/Nanbeige4.1-3B-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-o-4_5` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-o-4_5-gguf` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-V-4.6-Thinking` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-V-4.6-BNB` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-V-4.6-Thinking-gguf` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-SALA` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/AgentCPM-Report` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/AgentCPM-Report-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-V-4.6` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-V-4.6-GPTQ` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-V-4.6-Thinking` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-V-4.6-gguf` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `openbmb/MiniCPM-V-4.6-Thinking-gguf` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `CohereLabs/North-Mini-Code-1.0` | `blocked` | blocked by current local runtime support | `reports/model-radar/north-mini-code-gguf-current-release-scan-20260612.md`<br>`reports/runtime/north-mini-code-gguf-q4km-smoke-20260612.md` |
| hermes | `unsloth/North-Mini-Code-1.0-GGUF` | `blocked` | blocked by current local runtime support | `reports/model-radar/north-mini-code-gguf-current-release-scan-20260612.md`<br>`reports/runtime/north-mini-code-gguf-q4km-smoke-20260612.md` |
| hermes | `deepseek-ai/DeepSeek-V4-Pro` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `nvidia/LocateAnything-3B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `bosonai/higgs-audio-v3-tts-4b` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3.6-27B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3.6-27B-FP8` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `unsloth/Qwen3.6-27B-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `unsloth/Qwen3.6-27B-UD-MLX-4bit` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `unsloth/Qwen3.6-27B-MTP-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `byteshape/Qwen3.6-35B-A3B-MTP-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `LiquidAI/LFM2.5-8B-A1B-GGUF` | `blocked` | blocked by strict Hermes tool-call formatting failure | `reports/benchmark/local-pilots/lfm25-8b-a1b-q4km-llamacpp-strict-bfcl-pilot-20260613.md`<br>`reports/runtime/lfm25-8b-a1b-q4km-llamacpp-smoke-20260612.md` |
| hermes | `LiquidAI/LFM2.5-350M` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `LiquidAI/LFM2.5-VL-450M` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `LiquidAI/LFM2.5-Audio-1.5B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `LiquidAI/LFM2-8B-A1B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-Next-80B-A3B-Instruct` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `jinaai/jina-embeddings-v4` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-VL-Embedding-2B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-VL-Embedding-8B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Qwen/Qwen3-VL-Reranker-8B` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mlx-community/Qwen3-VL-Embedding-2B-8bit` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `aiteza/Qwen3-VL-Embedding-8B-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `mradermacher/Qwen3-VL-Reranker-8B-GGUF` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `Zeknes/Qwen3-VL-Reranker-8B-MLX-4bit` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `jinaai/jina-embeddings-v5-omni-small` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `jinaai/jina-embeddings-v5-omni-nano` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `jinaai/jina-embeddings-v5-omni-small-mlx` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `jinaai/jina-embeddings-v5-omni-nano-mlx` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `jinaai/jina-embeddings-v5-omni-nano-retrieval-mlx` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `onnx-community/jina-embeddings-v5-omni-nano-ONNX` | `blocked` | blocked until runtime artifact/load proof exists |  |
| hermes | `BlinkDL/rwkv7-g1` | `blocked` | blocked because open local weights or a supported public runtime are not verified |  |
| hermes | `BlinkDL/rwkv-7-world` | `blocked` | blocked because open local weights or a supported public runtime are not verified |  |
| hermes | `state-spaces/mamba-3-watchlist` | `blocked` | blocked because open local weights or a supported public runtime are not verified |  |
| hermes | `mit-oasys/rlm-qwen3-8b-v0.1` | `blocked` | blocked because open local weights or a supported public runtime are not verified |  |
| mem0 | `google/embeddinggemma-300m` | `blocked` | blocked on gated/authenticated model access | `reports/benchmark/mem0/embedding-google-embeddinggemma-300m-blocked-20260612.md` |
| mem0 | `jinaai/jina-embeddings-v4` | `blocked` | blocked by current local runtime support |  |
| mem0 | `hermes3:8b` | `blocked` | blocked by local timeout/stall; needs cloud/offload or narrower harness | `reports/benchmark/endpoint-tool-call/hermes3-8b-ollama-heldout-20260524.md`<br>`reports/benchmark/mem0/extraction-hermes3-8b-expanded-examples-20260524.md`<br>`reports/benchmark/mem0/run-cards/extraction-hermes3-8b-expanded-examples-20260524.md` |

## Every Candidate

| Project | Candidate | Role | Status | Benchmark kind | Coverage | Appropriateness / next gate |
|---|---|---|---|---|---|---|
| hermes | `Qwen/Qwen3.6-35B-A3B` | cloud-teacher | `ready` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked by strict Hermes tool-call formatting failure |
| hermes | `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `deepsweet/Qwen3.6-35B-A3B-MLX-oQ4` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `NousResearch/Hermes-4-14B` | cloud-teacher | `ready` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `benchmarked-not-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| hermes | `qwen3.7-open-weights-watch` | watchlist | `speculative` | watchlist only | `blocked` | blocked because open local weights or a supported public runtime are not verified |
| hermes | `mlx-community/Qwen3-VL-32B-Instruct-4bit` | local-runtime | `needs-runtime-proof` | support-lane modality benchmark | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `NousResearch/Hermes-4.3-36B` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `NousResearch/Hermes-4.3-36B-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `DJLougen/Harmonic-9B` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `DJLougen/Harmonic-Hermes-9B-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mradermacher/Harmonic-Hermes-9B-i1-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mkadrlik/hermes-Qwen3.5-2B-SFT-v7` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mkadrlik/Hermes-27B-SFT-v7` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-4-12B-it` | local-finetune | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-4-12B` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `unsloth/gemma-4-12b-it-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `unsloth/gemma-4-12B-it-qat-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `batiai/gemma-4-12B-it-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-4-26B-A4B-it` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-4-31B-it` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-4-31B` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-4-E2B-it-qat-q4_0-gguf` | local-runtime | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by strict Hermes tool-call formatting failure |
| hermes | `google/gemma-4-E2B-it` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-4-E2B-it-qat-mobile-transformers` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `litert-community/gemma-4-E2B-it-litert-lm` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mlx-community/gemma-4-e2b-it-4bit` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by current local runtime support |
| hermes | `mlx-community/gemma-4-E4B-it-qat-4bit` | local-runtime | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by strict Hermes tool-call formatting failure |
| hermes | `google/gemma-4-E4B-it-qat-mobile-transformers` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `unsloth/gemma-4-26B-A4B-it-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `lmstudio-community/gemma-4-31B-it-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `unsloth/gemma-4-31B-it-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `ggml-org/gemma-4-31B-it-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `bartowski/google_gemma-4-31B-it-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-4-31B-it-qat-q4_0-gguf` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/Gemma-4-31B-IT-NVFP4` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/Gemma-4-26B-A4B-NVFP4` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-4B-MLX-4bit` | local-finetune | `needs-auth` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `smoke-or-pilot-only` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| hermes | `Qwen/Qwen3.5-0.8B` | local-finetune | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by empty/no-content generation under the strict prompt |
| hermes | `Qwen/Qwen3.5-2B` | local-finetune | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by empty/no-content generation under the strict prompt |
| hermes | `Qwen/Qwen3.5-9B` | local-finetune | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-4B-Instruct-2507` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-4B-Thinking-2507` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3.5-27B` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `CohereLabs/command-a-plus-05-2026-w4a4` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `stepfun-ai/Step-3.7-Flash` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nex-agi/Nex-N2-mini` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-Coder-Next-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-Coder-Next` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/Nemotron-3.5-Content-Safety` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/nemotron-3.5-asr-streaming-0.6b` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/Qwen3-Nemotron-235B-A22B-GenRM-2603` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-Base-BF16` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-GenRM` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/nemotron-speech-streaming-en-0.6b` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-ASR-1.7B` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-Omni-30B-A3B-Instruct` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-Omni-30B-A3B-Captioner` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `microsoft/Phi-4-multimodal-instruct` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `CohereLabs/cohere-transcribe-03-2026` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/parakeet-tdt-0.6b-v3` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/instant-nurec` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/omni-dreams-models` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/Nemotron-Labs-Diffusion-14B` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/Nemotron-Labs-Diffusion-VLM-8B` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/diffusiongemma-26B-A4B-it` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/diffusiongemma-26B-A4B-it-NVFP4` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mlx-community/diffusiongemma-26B-A4B-it-mxfp4` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `deepseek-ai/DeepSeek-V4-Flash` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `deepseek-ai/DeepSeek-V4-Flash-Base` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-3n-E4B` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `google/gemma-4-E2B` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `microsoft/Phi-4-mini-instruct` | local-finetune | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `ibm-granite/granite-4.1-3b` | local-finetune | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by strict Hermes tool-call formatting failure |
| hermes | `LGAI-EXAONE/EXAONE-4.0-1.2B` | local-finetune | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by strict Hermes tool-call formatting failure |
| hermes | `openbmb/MiniCPM5-1B-MLX` | local-finetune | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by empty/no-content generation under the strict prompt |
| hermes | `openbmb/MiniCPM5-1B-GGUF` | local-runtime | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by strict Hermes tool-call formatting failure |
| hermes | `Nanbeige/Nanbeige4.1-3B` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Mungert/Nanbeige4.1-3B-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-o-4_5` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-o-4_5-gguf` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-V-4.6-Thinking` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-V-4.6-BNB` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-V-4.6-Thinking-gguf` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-SALA` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/AgentCPM-Report` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/AgentCPM-Report-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-V-4.6` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-V-4.6-GPTQ` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-V-4.6-Thinking` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-V-4.6-gguf` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `openbmb/MiniCPM-V-4.6-Thinking-gguf` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `CohereLabs/North-Mini-Code-1.0` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by current local runtime support |
| hermes | `unsloth/North-Mini-Code-1.0-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by current local runtime support |
| hermes | `deepseek-ai/DeepSeek-V4-Pro` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `nvidia/LocateAnything-3B` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `bosonai/higgs-audio-v3-tts-4b` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3.6-27B` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3.6-27B-FP8` | cloud-teacher | `needs-runtime-proof` | cloud teacher/runtime smoke plus Hermes strict tool-call sample | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `unsloth/Qwen3.6-27B-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `unsloth/Qwen3.6-27B-UD-MLX-4bit` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `unsloth/Qwen3.6-27B-MTP-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `byteshape/Qwen3.6-35B-A3B-MTP-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `LiquidAI/LFM2.5-1.2B-Instruct` | local-finetune | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `smoke-or-pilot-only` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| hermes | `LiquidAI/LFM2.5-1.2B-Thinking` | local-finetune | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `benchmarked-not-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| hermes | `LiquidAI/LFM2.5-8B-A1B-GGUF` | local-runtime | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked by strict Hermes tool-call formatting failure |
| hermes | `LiquidAI/LFM2-24B-A2B` | local-runtime | `ready` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `smoke-or-pilot-only` | strict tool-call gate is appropriate for Hermes promotion; pilot ties must be broken with official/expanded suites |
| hermes | `LiquidAI/LFM2.5-350M` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `LiquidAI/LFM2.5-VL-450M` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `LiquidAI/LFM2.5-Audio-1.5B` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `LiquidAI/LFM2-8B-A1B` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `LiquidAI/LFM2-ColBERT-350M` | retrieval | `needs-runtime-proof` | mem0 retrieval / embedding-reranking benchmark | `smoke-or-pilot-only` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| hermes | `Qwen/Qwen3-Next-80B-A3B-Instruct` | research-runtime | `needs-runtime-proof` | specialist runtime proof | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `microsoft/bitnet-b1.58-2B-4T` | research-runtime | `ready` | specialist runtime proof | `smoke-or-pilot-only` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| hermes | `jinaai/jina-embeddings-v4` | retrieval | `needs-runtime-proof` | mem0 retrieval / embedding-reranking benchmark | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-Embedding-4B` | retrieval | `needs-runtime-proof` | mem0 retrieval / embedding-reranking benchmark | `benchmarked-not-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| hermes | `Qwen/Qwen3-Reranker-4B` | retrieval | `needs-runtime-proof` | mem0 retrieval / embedding-reranking benchmark | `benchmarked-not-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| hermes | `Qwen/Qwen3-VL-Embedding-2B` | retrieval | `needs-runtime-proof` | mem0 retrieval / embedding-reranking benchmark | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-VL-Embedding-8B` | retrieval | `needs-runtime-proof` | mem0 retrieval / embedding-reranking benchmark | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-VL-Reranker-8B` | retrieval | `needs-runtime-proof` | mem0 retrieval / embedding-reranking benchmark | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mlx-community/Qwen3-VL-Embedding-2B-8bit` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `aiteza/Qwen3-VL-Embedding-8B-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `mradermacher/Qwen3-VL-Reranker-8B-GGUF` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Zeknes/Qwen3-VL-Reranker-8B-MLX-4bit` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `Qwen/Qwen3-Embedding-0.6B` | retrieval | `ready` | mem0 retrieval / embedding-reranking benchmark | `benchmarked-not-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| hermes | `Qwen/Qwen3-Reranker-0.6B` | retrieval | `ready` | mem0 retrieval / embedding-reranking benchmark | `evidence-present-needs-review` | requires expanded/adversarial retrieval replay before default promotion |
| hermes | `jinaai/jina-embeddings-v5-omni-small` | retrieval | `needs-runtime-proof` | mem0 retrieval / embedding-reranking benchmark | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `jinaai/jina-embeddings-v5-omni-nano` | retrieval | `needs-runtime-proof` | mem0 retrieval / embedding-reranking benchmark | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `jinaai/jina-embeddings-v5-omni-small-mlx` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `jinaai/jina-embeddings-v5-omni-nano-mlx` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `jinaai/jina-embeddings-v5-omni-nano-retrieval-mlx` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `onnx-community/jina-embeddings-v5-omni-nano-ONNX` | local-runtime | `needs-runtime-proof` | Hermes strict tool-call, local pilots, runtime smoke, selected lm-eval | `blocked` | blocked until runtime artifact/load proof exists |
| hermes | `BAAI/bge-m3` | retrieval | `ready` | mem0 retrieval / embedding-reranking benchmark | `evidence-present-needs-review` | requires expanded/adversarial retrieval replay before default promotion |
| hermes | `BlinkDL/rwkv7-g1` | watchlist | `speculative` | watchlist only | `blocked` | blocked because open local weights or a supported public runtime are not verified |
| hermes | `BlinkDL/rwkv-7-world` | watchlist | `speculative` | watchlist only | `blocked` | blocked because open local weights or a supported public runtime are not verified |
| hermes | `state-spaces/mamba-3-watchlist` | watchlist | `speculative` | watchlist only | `blocked` | blocked because open local weights or a supported public runtime are not verified |
| hermes | `mit-oasys/rlm-qwen3-8b-v0.1` | watchlist | `speculative` | watchlist only | `blocked` | blocked because open local weights or a supported public runtime are not verified |
| mem0 | `nomic-embed-text:latest` | embedder | `working-default` | embedding retrieval suite plus collection migration proof | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `BAAI/bge-m3` | embedder | `benchmarked-cpu-mps-not-promoted` | embedding retrieval suite plus collection migration proof | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `google/embeddinggemma-300m` | embedder | `access-gated` | embedding retrieval suite plus collection migration proof | `blocked` | blocked on gated/authenticated model access |
| mem0 | `jinaai/jina-embeddings-v4` | embedder | `runtime-blocked` | embedding retrieval suite plus collection migration proof | `blocked` | blocked by current local runtime support |
| mem0 | `jinaai/jina-embeddings-v5-omni-small-mlx` | embedder | `source-model-benchmarked` | embedding retrieval suite plus collection migration proof | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` | embedder | `source-model-benchmarked` | embedding retrieval suite plus collection migration proof | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `Qwen/Qwen3-Embedding-4B` | embedder | `source-model-benchmarked` | embedding retrieval suite plus collection migration proof | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `Qwen/Qwen3-Reranker-4B` | reranker | `source-model-benchmarked` | fixed reranking suite, expanded replay, live multi-result fixture | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `onnx-community/Qwen3-Reranker-0.6B-ONNX` | reranker | `source-model-benchmarked` | fixed reranking suite, expanded replay, live multi-result fixture | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` | reranker | `isolated-fixture-proven` | fixed reranking suite, expanded replay, live multi-result fixture | `benchmarked-not-necessarily-promoted` | requires expanded/adversarial retrieval replay before default promotion |
| mem0 | `flaglow/BAAI-bge-reranker-v2-m3-mlx-fp16` | reranker | `candidate-runtime-id-verified` | fixed reranking suite, expanded replay, live multi-result fixture | `smoke-or-pilot-only` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `mem0-created-at-rank-reranker` | reranker | `live-read-wrapper-smoked` | fixed reranking suite, expanded replay, live multi-result fixture | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `LiquidAI/LFM2-ColBERT-350M` | retriever | `source-model-benchmarked` | late-interaction retriever suite plus separate index proof | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `sam860/LFM2:2.6b` | extractor | `working-default-clean-root-smoked` | memory extraction JSON/durability suite | `benchmarked-not-necessarily-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
| mem0 | `hermes3:8b` | extractor | `installed-baseline` | memory extraction JSON/durability suite | `blocked` | blocked by local timeout/stall; needs cloud/offload or narrower harness |
| mem0 | `NousResearch/Hermes-4-14B` | extractor | `extraction-benchmarked-not-promoted` | memory extraction JSON/durability suite | `benchmarked-not-promoted` | smoke/pilot evidence is useful for liveness but not sufficiently discriminating for promotion |
