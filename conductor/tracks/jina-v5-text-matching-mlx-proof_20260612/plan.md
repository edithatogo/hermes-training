# Plan: Jina v5 Text-Matching MLX Proof

## Phase 1: Loader Support

- [x] Task: support direct `model.py` Jina MLX repos when `utils.py` is absent.
- [x] Task: add unit coverage for direct model loading.

## Phase 2: Runtime Proof

- [x] Task: run the 3-case text-matching smoke from SSD-backed model artifacts.
- [x] Task: generate mem0 run card and refreshed benchmark index.

## Phase 3: Documentation And Validation

- [x] Task: update runtime proof queue and mem0 candidate notes.
- [x] Task: run focused tests, full tests, readiness validation, and syntax
  checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: text-matching smoke passed 3/3 with top-1 1.000, recall@3 1.000,
  MRR 1.000, nDCG@3 1.000, 1024-dimensional embeddings, and p50 embedding
  latency 0.022s.
- Gaps: Jina remains a candidate only; no default mem0 collection switch is
  made by this track.

