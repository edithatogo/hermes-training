# Plan: Gemma 4 E2B-it Packaging Refresh

## Phase 1: Source Verification

- [x] Task: confirm the official `google/gemma-4-E2B-it` page and the newest
  LiteRT/MLX packaging lanes from the live Hugging Face search.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the new Gemma 4 E2B-it
  entries.
- [x] Task: update `FUTURE_MODELS.md`, `HANDOFF.md`, and the current release
  scan note.
- [x] Task: add a follow-up scan report and track record for the E2B-it
  packaging refresh.

## Phase 3: Validation

- [x] Task: run candidate validation and repository whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: 9.6 / 10
- Evidence: source-backed official repo plus Mac-local packaging candidates.
- Gaps: runtime proof is intentionally out of scope for this slice.
