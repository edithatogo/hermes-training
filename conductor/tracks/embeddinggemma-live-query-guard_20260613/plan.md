# Implementation Plan

## Phase 1: Harness Isolation

- [x] Task: Isolate mem0 fixture subprocess state
    - [x] Create an output-local `$HOME/.mem0` copy for fixture runs.
    - [x] Call `mem0_wrapper.py` directly for add/search actions.
    - [x] Preserve active Python user-site and Homebrew dependency paths through
      `PYTHONPATH`.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Live Fixture Evidence

- [x] Task: Run fresh EmbeddingGemma live fixture
    - [x] Use the resilient llama.cpp embedding proxy.
    - [x] Keep fixture Qdrant, history, and logs on `/Volumes/PortableSSD`.
    - [x] Verify top-1 `1.000` and recall@3 `1.000`.
- [x] Task: Update documentation
    - [x] Generate run card.
    - [x] Update mem0 benchmark summary and index.
    - [x] Update model radar/future-model notes.
- [x] Task: Validate
    - [x] Run focused mem0 unit tests.
    - [x] Run mem0 evidence validator.
    - [x] Run mem0 model-candidate validator.
    - [x] Run hub readiness validation.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Health Target

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: live fixture pass at top-1 `1.000` and recall@3 `1.000`, guarded
  strategy pass at `1.000`, SSD-local artifacts, stopped server processes,
  focused tests, mem0 evidence validation, model-candidate validation, and hub
  readiness.
- Remaining gaps: default promotion still needs a deliberate resilient-proxy
  integration plan, rollback proof, and collection migration decision.
