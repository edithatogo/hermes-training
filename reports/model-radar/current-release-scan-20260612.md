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
| Gemma | `google/gemma-4-12B-it`, `google/gemma-4-12B`, `unsloth/gemma-4-12b-it-GGUF`, `unsloth/gemma-4-12B-it-qat-GGUF` | New mid-size Gemma 4 family members that are more plausible Mac/Colab candidates than the larger 26B/31B variants. |
| Qwen | `Qwen/Qwen3.5-9B` | Useful mid-size Qwen step between the already-tested tiny lanes and the larger Qwen3.6 frontier packages. |
| MiniCPM | `openbmb/MiniCPM5-1B` | Official 1B release remains a valid tiny helper/extractor candidate. |
| BitNet | `microsoft/bitnet-b1.58-2B-4T` and the existing BitNet ecosystem | Keep as a specialist runtime/research lane; local runtime proof exists, but Hermes compliance still blocks promotion. |

## Watchlist Status

- No verified open-weight `Qwen/Qwen3.7-*` repository surfaced in the official
  Hugging Face search checked for this refresh.
- The Harmonic-9B backbone and Harmonic-Hermes-9B GGUF packaging are now
  verified and should be treated as the new Hermes-style local runtime lane for
  this refresh.
- The Gemma 4 12B family now has verified Unsloth GGUF and QAT packaging, so
  the 12B lane is no longer just a native Transformers reference.
- That means Qwen3.7 remains watchlist-only until an actual open-weight repo or
  supported hosted workflow is published.

## Decision

- Add the verified 12B Gemma 4, Hermes 4.3, and Qwen3.5-9B entries to the
  machine-readable radar.
- Add the Harmonic-9B backbone and Harmonic-Hermes-9B packaging to the
  machine-readable radar.
- Add the Gemma 4 12B Unsloth GGUF and QAT packaging to the machine-readable
  radar.
- Keep Qwen3.7 on the watchlist.
- Treat everything here as source verification only; runtime proof remains a
  separate gate.
