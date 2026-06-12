# Multimodal Support Follow-Up - 2026-06-12

## Summary

This follow-up scan captures the newest multimodal repos that matter as support
lanes for Hermes-agent workflows.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| Qwen | `Qwen/Qwen3-Omni-30B-A3B-Instruct` | Official multimodal checkpoint for text, image, audio, and video workflows. |
| Qwen | `Qwen/Qwen3-Omni-30B-A3B-Captioner` | Audio-captioning specialization derived from Qwen3-Omni. |
| Microsoft | `microsoft/Phi-4-multimodal-instruct` | Compact multimodal foundation model useful for speech/image comparison. |

## Watchlist Status

- These are support lanes, not Hermes text/chat targets.
- Runtime proof remains a separate gate if any of them are used locally.

## Decision

- Add the new multimodal repos to `MODEL_CANDIDATES.yaml`.
- Update the radar docs to keep them in the support/runtime bucket.
