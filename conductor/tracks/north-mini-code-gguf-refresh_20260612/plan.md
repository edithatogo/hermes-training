# Plan: North-Mini-Code GGUF Packaging Refresh

## Phase 1: Source Verification

- [x] Task: confirm the fresh `unsloth/North-Mini-Code-1.0-GGUF` model card
  from the live Hugging Face search.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the new GGUF packaging entry.
- [x] Task: update `FUTURE_MODELS.md`, `HANDOFF.md`, and the current release
  scan note.
- [x] Task: add a follow-up scan report and track record for the packaging
  refresh.

## Phase 3: Validation

- [x] Task: run candidate validation and repository whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: 9.5 / 10
- Evidence: the lane is source-backed and useful for future runtime gating.
- Gaps: the runtime remains blocked by missing `cohere2moe` support.
