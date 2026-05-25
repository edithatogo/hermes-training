# Plan: mem0 Guarded Read Wrapper

## Phase 1: Entrypoint

- [x] Task: add `scripts/mem0_read.py` with close-margin as the default mode.
- [x] Task: add vector and Qwen comparison modes.
- [x] Task: add optional Qwen-to-vector fallback.

## Phase 2: Tests and Documentation

- [x] Task: cover strategy selection, default behavior, and fallback behavior.
- [x] Task: document wrapper usage and rollback boundaries.
- [x] Task: run a live read-only smoke from the SSD-backed Ollama root.

## Phase 3: Validation

- [x] Task: run the full unit and readiness gates.
- [x] Task: stop local services after validation.
- [x] Task: mark the track complete and push.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: code, unit tests, docs, and a live read-only smoke exist. The live
  smoke exited `0`, returned one result, confirmed read-only/no-config-mutation
  fields, and completed in `2.865s`.
- Gaps: future integration still needs Hermes-agent UX latency checks before
  wiring the wrapper into an always-on runtime.
