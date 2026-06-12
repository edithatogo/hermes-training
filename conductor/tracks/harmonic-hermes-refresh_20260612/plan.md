# Plan: Harmonic Hermes Refresh

## Phase 1: Source Verification

- [x] Task: verify the current Harmonic-9B and Harmonic-Hermes-9B Hugging Face pages.
- [x] Task: confirm the GGUF packaging paths are published.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the Harmonic family entries.
- [x] Task: update `FUTURE_MODELS.md` with the new Hermes-style local lane.
- [x] Task: update `HANDOFF.md` and the current release scan summary.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the lane is source-backed and directly useful for Hermes agent
  runtime comparison.
- Gaps: runtime proof still remains separate.
