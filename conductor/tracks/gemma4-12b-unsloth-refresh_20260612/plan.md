# Plan: Gemma 4 12B Unsloth Refresh

## Phase 1: Source Verification

- [x] Task: verify the current Gemma 4 12B and Unsloth packaging pages.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the Gemma 4 12B packaging entries.
- [x] Task: update `FUTURE_MODELS.md` with the 12B packaging comparison lanes.
- [x] Task: update `HANDOFF.md` and the current release scan summary.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the lane is source-backed and fits the Mac packaging comparison
  path.
- Gaps: runtime proof still remains separate.
