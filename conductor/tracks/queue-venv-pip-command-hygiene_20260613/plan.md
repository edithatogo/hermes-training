# Plan: Queue Venv Pip Command Hygiene

## Phase 1 - Command Templates

- [x] Task: Update runtime proof support-model install commands.
  - [x] Use `./.venv/bin/python -m pip` for `requirements-mem0-embeddings.txt`.

- [x] Task: Update mem0 reranker install commands.
  - [x] Use `./.venv/bin/python -m pip` for `requirements-mem0-rerankers.txt`.

## Phase 2 - Regression Coverage

- [x] Task: Add queue command assertions.
  - [x] Runtime support-model command cards require project-venv pip.
  - [x] mem0 cross-encoder reranker command cards require project-venv pip.
  - [x] Both tests reject bare `python -m pip install`.

## Phase 3 - Reports And Validation

- [x] Task: Regenerate runtime proof action queue reports.
- [x] Task: Regenerate mem0 candidate queue report.
- [x] Task: Run queue validators.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: Generated queues now install optional dependencies into the same virtualenv used to run their benchmark scripts.
- Validation: Focused queue tests, runtime queue validation, mem0 queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: No dependency installation or benchmark execution was performed.
- Decision: Complete. Command hygiene improved without changing model evidence.
