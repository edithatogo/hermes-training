# Implementation Plan

## Phase 1: Export And Harness

- [x] Task: Build copied live-store replay harness
    - [x] Export a bounded sample from default mem0 without mutation.
    - [x] Redact committed summaries while preserving private artifact paths.
    - [x] Re-embed copied memories into an EmbeddingGemma candidate profile.
    - [x] Compare default and candidate retrieval across representative queries.
- [x] Task: Add focused tests
    - [x] Validate result normalization for mem0 wrapper shapes.
    - [x] Validate redacted report generation excludes raw memory text.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Live Replay Evidence

- [x] Task: Run copied live-store replay
    - [x] Render a run-scoped EmbeddingGemma config.
    - [x] Run re-embed/search under the resilient llama.cpp proxy.
    - [x] Confirm proxy ports/processes stop afterward.
- [x] Task: Record evidence
    - [x] Write a redacted report under `reports/benchmark/mem0/`.
    - [x] Update mem0 docs and candidate state.
    - [x] Update the track plan and registry status.
- [x] Task: Validate
    - [x] Run focused tests.
    - [x] Run mem0 evidence/model-candidate checks as relevant.
    - [x] Run `scripts/validate_readiness.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Health Target

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: copied live-store replay ran against a bounded `default_user` /
  `codex` sample, committed only redacted evidence, left the default collection
  unchanged, and blocked promotion because top-1 match was `0.200` despite
  default-top recall `1.000`.
- Remaining gaps: a future track can test query rewriting, reranking, or an
  explicit migration policy if accepting changed ordering becomes desirable.
