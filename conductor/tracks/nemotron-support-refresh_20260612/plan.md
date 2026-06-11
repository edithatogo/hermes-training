# Plan: Nemotron Support Model Refresh

## Phase 1: Source Verification

- [x] Task: verify the current published status of Nemotron 3.5 Content Safety
  and Nemotron 3.5 streaming ASR.
- [x] Task: confirm whether an MLX conversion exists for the ASR model.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the verified support lanes.
- [x] Task: update `FUTURE_MODELS.md` with the support-lane guidance.
- [x] Task: update `HANDOFF.md` with the new specialist support summary.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.5 / 10`
- Evidence: the refresh is source-backed and keeps support models out of the
  Hermes text lane.
- Gaps: no runtime proof is claimed for either support model.
