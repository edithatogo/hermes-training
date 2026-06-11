# Plan: Model Radar Tiny/Small Refresh

## Phase 1: Live Radar Refresh

- [x] Task: refresh tiny/small model candidates in `MODEL_CANDIDATES.yaml` and
  `FUTURE_MODELS.md`.
- [x] Task: record external compute lane updates in `PLATFORM_LANES.md`.

## Phase 2: mem0 And Runtime Proof Queue

- [x] Task: add Jina v5 omni MLX mem0 candidate, collection, and queue-command
  support.
- [x] Task: add runtime proof queue entries for Qwen3.5, North Mini Code, and
  Jina MLX candidates.
- [x] Task: preserve blocked-preflight status for unproven models and
  completed-runtime-proof status only where smoke evidence exists.

## Phase 3: Validation And Documentation

- [x] Task: add unit coverage for the Jina MLX candidate queue command.
- [x] Task: include the new scripts in readiness syntax checks and sync the
  model-radar contract environment list.
- [x] Task: run schema checks, unit tests, readiness validation, and commit the
  scoped radar update.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: candidate entries are sourced from live HF/Artificial Analysis
  checks, Jina MLX local smoke evidence exists, new candidates stay behind
  runtime-proof gates, and schema/unit/readiness validation passes.
- Gaps: no newly listed candidate is promoted to default or publication status
  by this track.
