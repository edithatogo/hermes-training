# Plan: Gemma 4 31B and MiniCPM-o 4.5 Packaging Refresh

## Phase 1: Source Verification

- [x] Task: confirm the official `google/gemma-4-31B-it-qat-q4_0-gguf` and
  `openbmb/MiniCPM-o-4_5-gguf` model cards from the live Hugging Face search.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the new packaging entries.
- [x] Task: update `FUTURE_MODELS.md`, `HANDOFF.md`, and the current release
  scan note.
- [x] Task: add a follow-up scan report and track record for the packaging
  refresh.

## Phase 3: Validation

- [x] Task: run candidate validation and repository whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: 9.6 / 10
- Evidence: explicit packaging lanes for comparison and runtime triage.
- Gaps: runtime proof is intentionally out of scope for this slice.
