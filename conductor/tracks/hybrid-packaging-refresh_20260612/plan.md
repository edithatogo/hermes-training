# Plan: Hybrid Attention and Quantized Packaging Refresh

## Phase 1: Source Verification

- [x] Task: verify the current published status of MiniCPM-SALA, Gemma 4 31B
  NVFP4 packaging, and DeepSeek-V4-Flash-Base.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the verified candidates.
- [x] Task: update `FUTURE_MODELS.md` with the hybrid attention and packaging
  notes.
- [x] Task: update `HANDOFF.md` with the new guidance.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is conservative and keeps the models in teacher or
  specialist lanes.
- Gaps: no runtime proof is claimed for any newly added model.
