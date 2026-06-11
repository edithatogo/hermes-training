# Plan: Specialist Frontier Agentic Refresh

## Phase 1: Source Verification

- [x] Task: verify the current published status of Command A+, Step 3.7 Flash,
  and Nex-N2-mini.
- [x] Task: confirm whether local MLX conversion paths exist for Nex-N2-mini.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the verified agentic frontier
  candidates.
- [x] Task: update `FUTURE_MODELS.md` with the specialist frontier section.
- [x] Task: update `HANDOFF.md` with the new specialist guidance.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.5 / 10`
- Evidence: the refresh is conservative and keeps the large models in teacher
  or specialist lanes.
- Gaps: no runtime proof is claimed for any newly added model.
