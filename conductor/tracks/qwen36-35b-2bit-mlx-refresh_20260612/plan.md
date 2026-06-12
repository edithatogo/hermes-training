# Plan: Qwen3.6 35B 2-bit MLX Refresh

## Phase 1: Source Verification

- [x] Task: verify the current ManiacLabs 2-bit MLX pack page.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the ManiacLabs entry.
- [x] Task: update `FUTURE_MODELS.md` with the new local runtime lane.
- [x] Task: update `HANDOFF.md` and the current release scan summary.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, shortlist, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the pack is source-backed and directly useful for Apple Silicon.
- Gaps: runtime proof still remains separate.
