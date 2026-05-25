# Plan: mem0 Isolated Fixture Rerank Proof

## Phase 1: Benchmark Support

- [x] Task: extend the memory add/search benchmark to support close-margin and
  warm Qwen3 reranking.
- [x] Task: add unit coverage for reranked memory scoring.

## Phase 2: Fixture Runs

- [x] Task: run the close-margin reranker in the `hermes_fixture` namespace.
- [x] Task: run warm Qwen3 0.6B in the `hermes_fixture` namespace.
- [x] Task: confirm cleanup deleted all temporary fixture memories.

## Phase 3: Documentation and Gates

- [x] Task: document fixture results, run cards, and next gates.
- [x] Task: update model radar, benchmark index, handoff, and Conductor status.
- [x] Task: run final validation and push.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: raw fixture add/search pass stayed at `0.400`, while both
  close-margin and warm Qwen3 reranking passed `1.000`; cleanup succeeded for
  `11/11` temporary memories in both runs. Structural readiness and the full
  unit suite passed after documentation updates.
- Gaps: this is namespace isolation only; the stronger config-isolated fixture
  gate is tracked separately.
