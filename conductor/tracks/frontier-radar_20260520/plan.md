# Plan: Frontier Model Radar and Bleeding-Edge Watchlist

## Phase 1 — Schema

- [x] Add role, environment, and feasibility fields to model candidates.
- [x] Add retrieval candidates beyond LFM2-ColBERT.
- [x] Add watchlist entries for RWKV and Mamba/subquadratic families.
- [x] Update validator behavior for speculative watchlist entries.

## Phase 2 — Verification

- [x] Run model candidate validation.
- [x] Review failed candidates and move unverified entries to watchlist.
- [x] Add quantization/runtime notes for Qwen3.6, Hermes 4, Gemma 4, Qwen3-Next, LFM2.5, BitNet, and retrieval models.

## Phase 3 — Promotion Rules

- [x] Add a radar refresh checklist to `NEW_MODEL_WORKFLOW.md`.
- [x] Add benchmark gate mapping by model role.
- [x] Add publication limits for teacher-only and runtime-only models.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: schema exists, validator skips speculative entries, verified candidate validation passes, and promotion-rule docs now name the role gates and publication limits.
- Gaps: none blocking; watchlist entries remain speculative by design.
- Decision: ready for review after the docs refresh.
