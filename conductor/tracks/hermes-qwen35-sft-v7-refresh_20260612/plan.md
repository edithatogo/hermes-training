# Plan: Hermes-Qwen3.5 SFT v7 Refresh

## Phase 1: Source Verification

- [x] Task: verify the current Hermes-Qwen3.5 SFT v7 pack pages.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the Hermes-Qwen3.5 packs.
- [x] Task: update `FUTURE_MODELS.md` with the new Hermes runtime lane.
- [x] Task: update `HANDOFF.md` and the current release scan summary.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, shortlist, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the packs are source-backed and directly useful for Hermes-local
  runtime comparisons.
- Gaps: runtime proof still remains separate.
