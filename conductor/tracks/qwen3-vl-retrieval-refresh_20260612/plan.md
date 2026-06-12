# Plan: Qwen3-VL Multimodal Retrieval Refresh

## Phase 1: Source Verification

- [x] Task: confirm the official `Qwen/Qwen3-VL-Embedding-2B`,
  `Qwen/Qwen3-VL-Embedding-8B`, and `Qwen/Qwen3-VL-Reranker-8B` model cards
  plus the latest MLX/GGUF packaging lanes from the live Hugging Face search.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the new Qwen3-VL entries.
- [x] Task: update `FUTURE_MODELS.md`, `HANDOFF.md`, and the current release
  scan note.
- [x] Task: add a follow-up scan report and track record for the multimodal
  retrieval refresh.

## Phase 3: Validation

- [x] Task: run candidate validation and repository whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: 9.6 / 10
- Evidence: source-backed multimodal retrieval baseline plus Mac-local
  packaging candidates.
- Gaps: runtime proof is intentionally out of scope for this slice.
