# Plan: Gemma 4 31B and MiniCPM5-1B Packaging Follow-up

## Phase 1: Source Verification

- [x] Task: confirm the fresh `unsloth/gemma-4-31B-it-GGUF`,
  `ggml-org/gemma-4-31B-it-GGUF`, and `openbmb/MiniCPM5-1B-GGUF` model cards
  from the live Hugging Face search.

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
- Evidence: the follow-up adds concrete packaging/runtime comparison points for
  the most relevant Gemma 4 31B and MiniCPM5 lanes.
- Gaps: runtime proof is intentionally out of scope for this slice.
