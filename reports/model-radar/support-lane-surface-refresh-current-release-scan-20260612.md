# Support Lane Surface Refresh - 2026-06-12

## Summary

This refresh captures the newest support-lane models that surfaced in the
official Hugging Face search and are relevant to Hermes-adjacent workflows on
MacBook Pro M1-class hardware or cloud teacher lanes.

## Verified Open-Weight Candidates

| Family | Verified release | Why it matters |
|---|---|---|
| DeepSeek | `deepseek-ai/DeepSeek-V4-Pro` | Fresh long-context MoE teacher/reference from the DeepSeek V4 preview line. Keep it in the cloud-teacher lane rather than trying to local-fit it. |
| NVIDIA | `nvidia/LocateAnything-3B` | Fresh vision-language grounding model for GUI localization and visual helper workflows. Useful for multimodal Hermes agent support. |
| Boson AI | `bosonai/higgs-audio-v3-tts-4b` | Fresh speech synthesis / voice-agent model with a strong audio helper profile. Useful for future Hermes voice workflows. |

## Watchlist Status

- DeepSeek V4 Pro is a cloud teacher/reference lane, not a 32GB local train target.
- LocateAnything-3B is a helper/support lane that needs runtime proof before any promotion.
- Higgs Audio v3 is a speech-support lane that also needs runtime proof before promotion.

## Decision

- Add `deepseek-ai/DeepSeek-V4-Pro` to the machine-readable radar.
- Add `nvidia/LocateAnything-3B` to the machine-readable radar.
- Add `bosonai/higgs-audio-v3-tts-4b` to the machine-readable radar.
- Keep all three as support lanes rather than automatic fine-tune targets.
