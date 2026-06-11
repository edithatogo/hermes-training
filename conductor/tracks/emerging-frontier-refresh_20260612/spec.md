# Specification: Emerging Frontier Multimodal and 1-Bit Refresh

## Overview

The Hermes radar needs a follow-up pass for the newest multimodal and
frontier-scale open-weight releases, plus the emerging 1-bit fine-tuning path.

This refresh focuses on:

- Gemma 4 31B-it as the larger Gemma 4 teacher baseline
- MiniCPM-o 4.5 as a multimodal helper/runtime lane
- DeepSeek-V4-Flash as a long-context cloud-teacher reference
- Nemotron Ultra 550B-A55B as the larger NVIDIA teacher baseline
- BitNet/QVAC BitLoRA support as an emerging 1-bit fine-tuning path

## Scope

- Verify the current published status of the new frontier candidates.
- Add the verified candidates to `MODEL_CANDIDATES.yaml`.
- Update `FUTURE_MODELS.md` and `HANDOFF.md` with the new guidance.
- Record a concise scan report of the new additions and guardrails.

## Out Of Scope

- No runtime proof claims for the new candidates.
- No training runs.
- No promotion of the new models to default local fine-tune targets.

## Acceptance Criteria

- The radar includes the new multimodal and 1-bit frontier candidates.
- The docs make clear these are teacher/runtime or specialist-only lanes.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed and keeps the larger models in teacher
  or specialist lanes.
- Remaining gap: runtime proof is still separate for every candidate.
