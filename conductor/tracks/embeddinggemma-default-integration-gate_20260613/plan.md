# Implementation Plan

## Phase 1: Runtime Profile And Rollback Design

- [x] Task: Define the opt-in EmbeddingGemma runtime profile
    - [x] Identify the tracked config surface for mem0 embedding provider selection.
    - [x] Wire or document the resilient llama.cpp proxy launch path.
    - [x] Preserve endpoint compatibility with llama.cpp, LM Studio, and other
      OpenAI-compatible embedding servers where feasible.
- [x] Task: Define rollback behavior
    - [x] Document the command or config path that restores
      `nomic-embed-text:latest`.
    - [x] Keep `mem0_nomic_768` as the live default collection unless explicitly
      promoted.
    - [x] Add a small rollback smoke or static validation check.
- [x] Task: Decide collection compatibility
    - [x] Record the EmbeddingGemma 768-dim evidence.
    - [x] Check whether reuse of `mem0_nomic_768` is valid or whether a new
      collection name is required.
    - [x] Write the migration rule for future default promotion.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Opt-In Smoke And Documentation

- [x] Task: Run bounded opt-in smoke
    - [x] Run add/search through the opt-in profile using SSD-local state.
    - [x] Confirm all server ports/processes stop afterward.
    - [x] Record summary artifacts under `/Volumes/PortableSSD/hermes-evals`.
- [x] Task: Update promotion evidence
    - [x] Create or update the mem0 run card.
    - [x] Update the mem0 benchmark index.
    - [x] Update `MODEL_CANDIDATES.yaml` and `FUTURE_MODELS.md`.
- [x] Task: Validate
    - [x] Run focused mem0 unit tests.
    - [x] Run `scripts/check_mem0_benchmark_evidence.py`.
    - [x] Run `scripts/check_model_candidates.py`.
    - [x] Run `scripts/validate_readiness.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Health Target

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: live fixture proof exists, opt-in config rendering exists, the
  candidate collection is separate at `mem0_embeddinggemma_300m_768`, rollback
  is `unset MEM0_CONFIG_PATH` to the unchanged nomic config, and the bounded
  opt-in profile smoke passed through the resilient llama.cpp proxy. The agent
  wrapper smoke also passed through `scripts/hermes_mem0_tool.py`.
- Remaining gaps: a future separate default-promotion track must copy/re-embed
  representative live memories, compare against the current default, and update
  the live config only if rollback smoke passes.
