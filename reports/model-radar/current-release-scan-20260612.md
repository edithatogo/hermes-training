# Current Release Scan - 2026-06-12

## Summary

This refresh rechecked the official Hugging Face pages and current model
searches for Hermes-adjacent open-weight candidates that matter on a MacBook
Pro M1 Max with 32 GB unified memory.

## Verified Open-Weight Candidates

| Family | Verified release | Why it matters |
|---|---|---|
| Hermes | `NousResearch/Hermes-4.3-36B` and `NousResearch/Hermes-4.3-36B-GGUF` | Newer public Hermes release than the 14B baseline; useful as teacher/runtime baseline only. |
| Hermes | `DJLougen/Harmonic-9B`, `DJLougen/Harmonic-Hermes-9B-GGUF`, `mradermacher/Harmonic-Hermes-9B-i1-GGUF` | Stage 2 agentic fine-tune on Harmonic-9B with direct GGUF local lanes; the closest new Hermes-style local runtime path in this refresh. |
| Hermes | `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`, `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`, `mkadrlik/hermes-Qwen3.5-2B-SFT-v7`, `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`, `mkadrlik/Hermes-27B-SFT-v7` | Fresh Hermes-style Qwen3.5 GGUF packs; the 9B lane is the main new local runtime comparison point. |
| Qwen | `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming` | Fresh 2-bit MLX local-runtime candidate with explicit tool-calling and agentic tags. |
| Gemma | `google/gemma-4-12B-it`, `google/gemma-4-12B`, `unsloth/gemma-4-12b-it-GGUF`, `unsloth/gemma-4-12B-it-qat-GGUF` | New mid-size Gemma 4 family members that are more plausible Mac/Colab candidates than the larger 26B/31B variants. |
| Gemma | `google/gemma-4-E2B-it`, `litert-community/gemma-4-E2B-it-litert-lm`, `mlx-community/gemma-4-e2b-it-4bit` | Official instruction-tuned E2B lane plus fresh LiteRT and MLX packaging. The smallest useful Gemma 4 follow-up to the q4_0 smoke. |
| Gemma / Qwen / MiniCPM | `google/gemma-4-31B`, `Qwen/Qwen3-Coder-Next`, `openbmb/MiniCPM-V-4.6-GPTQ` | Follow-up scan additions: official base repos and packaging lanes that matter for teacher/runtime comparisons. |
| Packaging | `google/gemma-4-31B-it-qat-q4_0-gguf`, `openbmb/MiniCPM-o-4_5-gguf` | Fresh GGUF packaging lanes surfaced in the latest model search. Strong local packaging comparison points for Gemma 4 31B and MiniCPM-o 4.5. |
| NVIDIA | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-Base-BF16`, `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-GenRM`, `nvidia/nemotron-speech-streaming-en-0.6b` | New base/evaluator and speech-support checkpoints from the Nemotron family. |
| NVIDIA | `nvidia/instant-nurec`, `nvidia/omni-dreams-models` | Fresh physical-AI / world-model support lanes from NVIDIA. |
| ASR | `Qwen/Qwen3-ASR-1.7B`, `CohereLabs/cohere-transcribe-03-2026`, `nvidia/parakeet-tdt-0.6b-v3` | Fresh speech-support lanes for transcription and streaming ASR. |
| TTS | `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`, `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` | Fresh speech-output lane with an explicit MLX Mac packaging path. |
| Multimodal | `Qwen/Qwen3-Omni-30B-A3B-Instruct`, `Qwen/Qwen3-Omni-30B-A3B-Captioner`, `microsoft/Phi-4-multimodal-instruct` | Fresh broad multimodal support lanes for text, image, audio, and video workflows. |
| Multimodal retrieval | `Qwen/Qwen3-VL-Embedding-2B`, `Qwen/Qwen3-VL-Embedding-8B`, `Qwen/Qwen3-VL-Reranker-8B`, `mlx-community/Qwen3-VL-Embedding-2B-8bit`, `aiteza/Qwen3-VL-Embedding-8B-GGUF`, `mradermacher/Qwen3-VL-Reranker-8B-GGUF`, `Zeknes/Qwen3-VL-Reranker-8B-MLX-4bit` | Official multimodal retrieval pair plus fresh GGUF and MLX packaging. Strong next-step lane for screenshot, document-image, and video retrieval on Hermes workflows. |
| Multimodal retrieval | `jinaai/jina-embeddings-v5-omni-small`, `jinaai/jina-embeddings-v5-omni-nano`, `jinaai/jina-embeddings-v5-omni-small-mlx`, `jinaai/jina-embeddings-v5-omni-nano-mlx`, `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx`, `jinaai/jina-embeddings-v5-omni-nano-retrieval-mlx`, `onnx-community/jina-embeddings-v5-omni-nano-ONNX` | Fresh Jina v5 omni multimodal retrieval family with MLX and browser/WebGPU packaging. Strong fit for Hermes cross-modal search and client-side retrieval. |
| Qwen | `Qwen/Qwen3.5-9B` | Useful mid-size Qwen step between the already-tested tiny lanes and the larger Qwen3.6 frontier packages. |
| Embeddings | `google/embeddinggemma-300m`, `litert-community/embeddinggemma-300m`, `mlx-community/embeddinggemma-300m-4bit`, `lmstudio-community/embeddinggemma-300m-qat-GGUF` | Official Google embedding baseline plus fresh LiteRT, MLX, and GGUF packaging. Good as the next Hermes memory/RAG comparison point. |
| MiniCPM | `openbmb/MiniCPM5-1B` | Official 1B release remains a valid tiny helper/extractor candidate. |
| NVIDIA | `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16`, `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`, `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF`, `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | Official 4B base plus fresh GGUF and MLX packaging for Mac-local runtime use. |
| BitNet | `microsoft/bitnet-b1.58-2B-4T` and the existing BitNet ecosystem | Keep as a specialist runtime/research lane; local runtime proof exists, but Hermes compliance still blocks promotion. |

## Watchlist Status

- No verified open-weight `Qwen/Qwen3.7-*` repository surfaced in the official
  Hugging Face search checked for this refresh.
- The Harmonic-9B backbone and Harmonic-Hermes-9B GGUF packaging are now
  verified and should be treated as the new Hermes-style local runtime lane for
  this refresh.
- The Hermes-Qwen3.5 SFT v7 local packs are now verified and should be treated
  as a fresh Hermes-style comparison lane, with the 9B pack as the primary
  local runtime candidate.
- The ManiacLabs Qwen3.6 35B 2-bit MLX pack is now verified and should be
  treated as a fresh Qwen3.6 local-runtime candidate for Apple Silicon.
- The Gemma 4 12B family now has verified Unsloth GGUF and QAT packaging, so
  the 12B lane is no longer just a native Transformers reference.
- The official Gemma 4 E2B-it lane is now surfaced, along with LiteRT and MLX
  packaging, and should be treated as the smallest practical Gemma 4
  comparison point for Mac-local helper workflows.
- The official `google/embeddinggemma-300m` retrieval baseline is now surfaced
  along with LiteRT, MLX, and GGUF packaging. Treat it as the next Hermes
  memory/RAG comparison point.
- The follow-up scan also surfaced the official Gemma 4 31B base repo, the
  official Qwen3-Coder-Next base repo, a MiniCPM-V-4.6 GPTQ packaging lane, and
  the explicit Gemma 4 31B QAT GGUF and MiniCPM-o 4.5 GGUF packaging lanes.
- The latest NVIDIA pass surfaced the Nemotron 3 Ultra base checkpoint, the
  Nemotron 3 Ultra GenRM checkpoint, and the English streaming ASR checkpoint.
- The same pass also surfaced `nvidia/instant-nurec` and `nvidia/omni-dreams-models`
  as physical-AI / world-model support lanes.
- The latest ASR pass surfaced `Qwen/Qwen3-ASR-1.7B`,
  `CohereLabs/cohere-transcribe-03-2026`, and `nvidia/parakeet-tdt-0.6b-v3`.
- The same speech pass also surfaced `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`
  and `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16`.
- The broader multimodal pass also surfaced `Qwen/Qwen3-Omni-30B-A3B-Instruct`,
  `Qwen/Qwen3-Omni-30B-A3B-Captioner`, and `microsoft/Phi-4-multimodal-instruct`.
- The multimodal retrieval pass also surfaced `Qwen/Qwen3-VL-Embedding-2B`,
  `Qwen/Qwen3-VL-Embedding-8B`, `Qwen/Qwen3-VL-Reranker-8B`, plus MLX and
  GGUF packaging lanes for the 2B embedder and 8B embedder/reranker.
- The Jina omni retrieval pass also surfaced `jinaai/jina-embeddings-v5-omni-small`,
  `jinaai/jina-embeddings-v5-omni-nano`, MLX packaging for both sizes, and an
  ONNX browser/WebGPU lane for the nano model.
- That means Qwen3.7 remains watchlist-only until an actual open-weight repo or
  supported hosted workflow is published.

## Decision

- Add the verified 12B Gemma 4, Hermes 4.3, and Qwen3.5-9B entries to the
  machine-readable radar.
- Add the official Gemma 4 E2B-it base repo plus LiteRT and MLX packaging to
  the machine-readable radar.
- Add the official `google/embeddinggemma-300m` retrieval baseline plus LiteRT,
  MLX, and GGUF packaging to the machine-readable radar.
- Add the Harmonic-9B backbone and Harmonic-Hermes-9B packaging to the
  machine-readable radar.
- Add the Gemma 4 12B Unsloth GGUF and QAT packaging to the machine-readable
  radar.
- Add the Hermes-Qwen3.5 SFT v7 packs to the machine-readable radar.
- Add the ManiacLabs Qwen3.6 35B 2-bit MLX pack to the machine-readable radar.
- Add the official Nemotron 3 Nano 4B base plus GGUF and MLX packaging to the
  machine-readable radar.
- Add the Gemma 4 31B base repo, Qwen3-Coder-Next base repo, and
  MiniCPM-V-4.6-GPTQ packaging lane to the machine-readable radar.
- Add the Nemotron 3 Ultra base, Nemotron 3 Ultra GenRM, and English streaming
  ASR checkpoints to the machine-readable radar.
- Add `nvidia/instant-nurec` and `nvidia/omni-dreams-models` to the
  machine-readable radar as support lanes.
- Add `Qwen/Qwen3-ASR-1.7B`, `CohereLabs/cohere-transcribe-03-2026`, and
  `nvidia/parakeet-tdt-0.6b-v3` to the machine-readable radar as speech-support lanes.
- Add `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` and
  `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` to the machine-readable radar.
- Add `Qwen/Qwen3-Omni-30B-A3B-Instruct`, `Qwen/Qwen3-Omni-30B-A3B-Captioner`,
  and `microsoft/Phi-4-multimodal-instruct` to the machine-readable radar.
- Add the Qwen3-VL multimodal retrieval embedding and reranker pair plus the
  Mac packaging lanes to the machine-readable radar.
- Add the Jina v5 omni multimodal retrieval family and its MLX/browser lanes to
  the machine-readable radar.
- Add the Gemma 4 31B QAT GGUF and MiniCPM-o 4.5 GGUF packaging lanes to the
  machine-readable radar.
- Keep Qwen3.7 on the watchlist.
- Treat everything here as source verification only; runtime proof remains a
  separate gate.
