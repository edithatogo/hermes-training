# Plan: Nemotron Frontier Model Refresh

## Phase 1: Source Verification

- [x] Task: verify the published status of Nemotron 3 Nano Omni Reasoning,
  Nemotron 3 Super NVFP4, and Qwen3-Nemotron GenRM.
- [x] Task: confirm the reward-model / teacher role of Qwen3-Nemotron.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the verified frontier models.
- [x] Task: update `FUTURE_MODELS.md` with the Nemotron frontier section.
- [x] Task: update `HANDOFF.md` with the new frontier guidance.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.5 / 10`
- Evidence: the refresh is conservative and keeps the large models in teacher
  or reward-model lanes.
- Gaps: no runtime proof is claimed for any newly added model.
