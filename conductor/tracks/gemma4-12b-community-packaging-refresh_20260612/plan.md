# Plan: Gemma 4 12B Community Packaging Refresh

## Phase 1: Source Verification

- [x] Task: verify the current Gemma 4 12B community packaging and base pages.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the community packaging entries.
- [x] Task: update `FUTURE_MODELS.md` with the community packaging lanes.
- [x] Task: update `HANDOFF.md` and the current release scan summary.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the packaging is source-backed and directly useful for the Mac
  runtime lane.
- Gaps: runtime proof still remains separate.
