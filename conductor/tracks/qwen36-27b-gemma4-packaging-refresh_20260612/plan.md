# Plan: Qwen3.6-27B and Gemma 4 Packaging Refresh

## Phase 1: Source Verification

- [x] Task: verify the current published status of Qwen/Qwen3.6-27B,
  Qwen/Qwen3.6-27B-FP8, unsloth/Qwen3.6-27B-GGUF, and the current Gemma 4 12B
  and 31B packaging surface.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the verified candidates.
- [x] Task: update `FUTURE_MODELS.md` with the dense frontier and packaging
  notes.
- [x] Task: update `HANDOFF.md` with the new guidance.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is conservative and keeps the models in research or
  specialist lanes.
- Gaps: no runtime proof is claimed for any newly added model.
