# Plan: Support Lane Surface Refresh

## Phase 1: Source Verification

- [x] Task: confirm the fresh `deepseek-ai/DeepSeek-V4-Pro`,
  `nvidia/LocateAnything-3B`, and `bosonai/higgs-audio-v3-tts-4b` model cards
  from the live Hugging Face search.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the new support-lane entries.
- [x] Task: update `FUTURE_MODELS.md`, `HANDOFF.md`, and the current release
  scan note.
- [x] Task: add a follow-up scan report and track record for the support-lane
  refresh.

## Phase 3: Validation

- [x] Task: run candidate validation and repository whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: 9.5 / 10
- Evidence: the lanes are source-backed and immediately useful for deciding
  what should be kept as teacher, helper, or speech support.
- Gaps: runtime proof is intentionally out of scope.
