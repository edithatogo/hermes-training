# ASR Support Follow-Up - 2026-06-12

## Summary

This follow-up scan captures the newest official speech and transcription repos
that matter as support lanes for Hermes-agent workflows.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Qwen | `Qwen/Qwen3-ASR-1.7B` | Official streaming/offline ASR release with broad language coverage. |
| Cohere | `CohereLabs/cohere-transcribe-03-2026` | Fresh transcription model useful for audio support workflows. |
| NVIDIA | `nvidia/parakeet-tdt-0.6b-v3` | Multilingual ASR release useful as a transcription support lane. |

## Watchlist Status

- These are support lanes, not Hermes text/chat targets.
- Runtime proof remains a separate gate if any of them are used locally.

## Decision

- Add the new ASR repos to `MODEL_CANDIDATES.yaml`.
- Update the radar docs to keep them in the support/runtime bucket.
