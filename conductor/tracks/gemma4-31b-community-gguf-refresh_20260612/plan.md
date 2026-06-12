# Plan: Gemma 4 31B Community GGUF Refresh

## Phase 1: Source Verification

- [x] Task: confirm the fresh `bartowski/google_gemma-4-31B-it-GGUF` model
  card from the live Hugging Face search.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the new packaging entry.
- [x] Task: update `FUTURE_MODELS.md`, `HANDOFF.md`, and the current release
  scan note.
- [x] Task: add a follow-up scan report and track record for the community
  GGUF refresh.

## Phase 3: Validation

- [x] Task: run candidate validation and repository whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: 9.6 / 10
- Evidence: community GGUF packaging for local comparison and runtime triage.
- Gaps: runtime proof is intentionally out of scope for this slice.
