# Agentic Research and Diffusion Current Release Scan

Date: 2026-06-12

This follow-up scan extends the frontier radar with a deep-research agent and
the latest diffusion-style text and multimodal releases. It does not claim
runtime proof or training readiness.

## What Changed

- `openbmb/AgentCPM-Report` and `openbmb/AgentCPM-Report-GGUF` are now tracked
  as a deep-research agent lane.
- `openbmb/MiniCPM-V-4.6` and `openbmb/MiniCPM-V-4.6-gguf` are now tracked as
  edge-friendly multimodal helper lanes.
- `nvidia/Nemotron-Labs-Diffusion-14B` and `nvidia/Nemotron-Labs-Diffusion-VLM-8B`
  are now tracked as research/runtime lanes for diffusion-based decoding
  experiments.

## Radar Summary

| Model | Status | Recommended lane |
|---|---|---|
| `openbmb/AgentCPM-Report` | Verified official repo | Deep research / orchestration comparison lane |
| `openbmb/AgentCPM-Report-GGUF` | Verified GGUF packaging repo | Local runtime comparison only |
| `openbmb/MiniCPM-V-4.6` | Verified official repo | Multimodal helper/runtime lane |
| `openbmb/MiniCPM-V-4.6-gguf` | Verified GGUF packaging repo | Local multimodal runtime comparison only |
| `nvidia/Nemotron-Labs-Diffusion-14B` | Verified official repo | Speed/reasoning research lane |
| `nvidia/Nemotron-Labs-Diffusion-VLM-8B` | Verified official repo | Multimodal diffusion research lane |

## Guardrails

- Keep `Qwen3.7` watchlist-only until official open weights appear.
- Do not treat these models as default local fine-tune targets.
- Use the new research models only if the workflow needs long-horizon
  research, higher-resolution VLM work, or decoding-speed experiments.

## Sources

- OpenBMB AgentCPM-Report and AgentCPM-Report-GGUF model cards
- OpenBMB MiniCPM-V 4.6 and MiniCPM-V 4.6 GGUF model cards
- NVIDIA Nemotron-Labs-Diffusion 14B and VLM 8B model cards
