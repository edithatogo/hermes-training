# Plan: Emerging Frontier Multimodal and 1-Bit Refresh

## Phase 1: Source Verification

- [x] Task: verify the current published status of Gemma 4 31B-it, MiniCPM-o
  4.5, DeepSeek-V4-Flash, Nemotron Ultra, and the BitNet/QVAC fine-tune path.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the verified frontier
  candidates.
- [x] Task: update `FUTURE_MODELS.md` with the multimodal and 1-bit frontier
  notes.
- [x] Task: update `HANDOFF.md` with the new frontier guidance.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is conservative and keeps the larger models in teacher
  or specialist lanes.
- Gaps: no runtime proof is claimed for any newly added model.
