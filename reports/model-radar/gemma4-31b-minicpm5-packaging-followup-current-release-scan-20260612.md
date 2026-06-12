# Gemma 4 31B and MiniCPM5-1B Packaging Follow-up - 2026-06-12

## Summary

This follow-up refresh captured the fresh Gemma 4 31B and MiniCPM5 packaging
lanes that surfaced in the current Hugging Face search. The goal is to keep the
Hermes model radar anchored to real, Mac-usable local packaging options rather
than assuming the official base repos are the only practical path.

## Verified Open-Weight Candidates

| Family | Verified release | Why it matters |
|---|---|---|
| Gemma | `unsloth/gemma-4-31B-it-GGUF`, `ggml-org/gemma-4-31B-it-GGUF` | Fresh community Gemma 4 31B GGUF lanes with direct Ollama/llama.cpp style usage guidance. These are the newest packaging comparison points after the official QAT and bartowski packs. |
| MiniCPM | `openbmb/MiniCPM5-1B-GGUF` | Official GGUF packaging for the tiny MiniCPM5 helper/extractor lane. Good as a compact runtime comparison point for Hermes-adjacent workflows. |
| MiniCPM | `Abiray/MiniCPM5-1B-GGUF` | Community GGUF alternate for MiniCPM5-1B. Useful as a fallback packaging comparison point, but the official `openbmb` pack remains the canonical reference. |

## Watchlist Status

- The new Gemma 4 31B Unsloth and ggml-org GGUF packs are source-backed and
  ready for packaging/runtime comparison only.
- The official `openbmb/MiniCPM5-1B-GGUF` lane is now source-backed and should
  be treated as the canonical tiny GGUF path for MiniCPM5.
- The community `Abiray/MiniCPM5-1B-GGUF` pack is useful as a packaging
  alternate, but it should stay secondary to the official pack.
- No new Qwen3.7 open-weight lane was required for this follow-up.

## Decision

- Add the fresh Gemma 4 31B Unsloth GGUF lane to the machine-readable radar.
- Add the fresh Gemma 4 31B ggml-org GGUF lane to the machine-readable radar.
- Add the official `openbmb/MiniCPM5-1B-GGUF` lane to the machine-readable radar.
- Keep the `Abiray/MiniCPM5-1B-GGUF` pack documented as a community alternate only.
- Treat all of these as packaging/runtime comparison points, not automatic fine-tune targets.
