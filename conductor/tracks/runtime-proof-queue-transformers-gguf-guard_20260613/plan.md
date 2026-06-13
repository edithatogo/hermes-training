# Plan: Runtime Proof Queue Transformers GGUF Guard

## Phase 1 - Routing Fix

- [x] Task: Prioritize explicit `hf-transformers` environment.
  - [x] Move the Transformers command branch ahead of GGUF detection.
  - [x] Keep GGUF endpoint commands available for LM Studio/Ollama/GGUF candidates.

## Phase 2 - Regression Coverage

- [x] Task: Add a focused routing regression test.
  - [x] Use an `hf-transformers` candidate whose runtime text mentions GGUF.
  - [x] Assert it uses `run_transformers_pilot_benchmark.py`.
  - [x] Assert it does not use `run_endpoint_pilot_benchmark.py`.

## Phase 3 - Reports And Validation

- [x] Task: Regenerate runtime proof action queue artifacts.
- [x] Task: Validate the queue is current.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: Affected `hf-transformers` command cards now point to the bounded Transformers pilot, and regression coverage locks the behavior.
- Validation: Focused queue tests, runtime proof queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: No runtime proof was executed in this bugfix track.
- Decision: Complete. The queue is more executable and less error-prone.
