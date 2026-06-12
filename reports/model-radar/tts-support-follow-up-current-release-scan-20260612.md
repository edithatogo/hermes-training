# TTS Support Follow-Up - 2026-06-12

## Summary

This follow-up scan captures the newest official speech-generation repo and its
Mac-local packaging path.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Qwen | `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | Official voice-design and TTS repo with voice cloning and natural-language voice control support. |
| Qwen | `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` | MLX-packaged Mac-local speech-generation lane for Apple Silicon. |

## Watchlist Status

- These are speech-output support lanes, not Hermes chat targets.
- Runtime proof remains a separate gate if either is ever used locally.

## Decision

- Add the new TTS repos to `MODEL_CANDIDATES.yaml`.
- Update the radar docs to keep them in the support/runtime bucket.
