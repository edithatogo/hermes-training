# Frontier Teacher and Support Lane Evaluation

## Overview

Evaluate frontier, teacher, support, multimodal, audio, ASR, TTS, and packaging candidates from the completed scan report as separate support lanes. The goal is to make these models useful to Hermes and mem0 development without misclassifying oversized or specialized models as local fine-tune targets.

## Scope

- Review current scan-report additions and follow-up lanes:
  - frontier teacher/reference models
  - NVIDIA Nemotron and NGC-relevant support models
  - multimodal and retrieval support candidates
  - audio, ASR, TTS, and omni support candidates
  - quantized, hybrid-attention, mobile, and packaging-specific candidates
- Define usage boundaries for teacher generation, evaluation, retrieval augmentation, multimodal evidence extraction, or benchmark support.
- Use Colab, Azure, or NVIDIA/NGC only when the candidate and license make external execution appropriate.
- Keep local Mac/Metal feasibility separate from reference-only value.

## Out of Scope

- Treating large frontier models as local Hermes defaults.
- Running gated or paid models without credentials, license, and cost approval.
- Building production integrations for support lanes before benchmark value is shown.
- Publishing derived outputs from restricted models without review.

## Acceptance Criteria

- Each support-lane candidate has a role, backend feasibility, and next action.
- Teacher/reference candidates are clearly separated from local runtime and fine-tune candidates.
- NVIDIA/NGC-specific opportunities are linked to NGC preflight and entitlement requirements.
- Support lanes feed concrete benchmark or data-generation tasks rather than broad watchlist notes.

## Health Target

This track should not be marked complete below health 9.5. The final support-lane matrix must be actionable without over-promising local compatibility.
