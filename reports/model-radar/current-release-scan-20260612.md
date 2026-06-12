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
| Gemma / Qwen / MiniCPM | `google/gemma-4-31B`, `Qwen/Qwen3-Coder-Next`, `openbmb/MiniCPM-V-4.6-GPTQ` | Follow-up scan additions: official base repos and packaging lanes that matter for teacher/runtime comparisons. |
| NVIDIA | `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-Base-BF16`, `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-GenRM`, `nvidia/nemotron-speech-streaming-en-0.6b` | New base/evaluator and speech-support checkpoints from the Nemotron family. |
| NVIDIA | `nvidia/instant-nurec`, `nvidia/omni-dreams-models` | Fresh physical-AI / world-model support lanes from NVIDIA. |
| Qwen | `Qwen/Qwen3.5-9B` | Useful mid-size Qwen step between the already-tested tiny lanes and the larger Qwen3.6 frontier packages. |
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
- The follow-up scan also surfaced the official Gemma 4 31B base repo, the
  official Qwen3-Coder-Next base repo, and a MiniCPM-V-4.6 GPTQ packaging lane.
- The latest NVIDIA pass surfaced the Nemotron 3 Ultra base checkpoint, the
  Nemotron 3 Ultra GenRM checkpoint, and the English streaming ASR checkpoint.
- The same pass also surfaced `nvidia/instant-nurec` and `nvidia/omni-dreams-models`
  as physical-AI / world-model support lanes.
- That means Qwen3.7 remains watchlist-only until an actual open-weight repo or
  supported hosted workflow is published.

## Decision

- Add the verified 12B Gemma 4, Hermes 4.3, and Qwen3.5-9B entries to the
  machine-readable radar.
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
- Keep Qwen3.7 on the watchlist.
- Treat everything here as source verification only; runtime proof remains a
  separate gate.
