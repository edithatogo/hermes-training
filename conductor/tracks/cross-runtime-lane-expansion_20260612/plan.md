# Plan: Cross Runtime Lane Expansion

## Phase 1: Runtime Tool Audit

- [x] Task: inventory the current runtime tooling references and packaging lanes in the radar and handoff docs.
- [x] Task: capture the practical fit for `llama.cpp`, Ollama, LM Studio, MLX, Metal, Colab, Azure, Kaggle, and NVIDIA tooling.
- [x] Task: note which lanes are available, which are conditional, and which are still blocked.
- [x] Task: Conductor - Automated Review and Checkpoint 'Runtime Tool Audit' (Protocol in workflow.md)

## Phase 2: Runtime Matrix Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` and the roadmap docs with the runtime-lane classification.
- [x] Task: keep external execution lanes documented as options rather than default dependencies.
- [x] Task: preserve the Mac/Metal-first lane while noting cloud and hosted alternatives.
- [x] Task: Conductor - Automated Review and Checkpoint 'Runtime Matrix Sync' (Protocol in workflow.md)

## Phase 3: Validation

- [x] Task: run candidate validation and markdown/repo sanity checks.
- [x] Task: capture the final runtime-lane matrix and the next proof candidates.
- [x] Task: Conductor - Automated Review and Checkpoint 'Validation' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: the track makes the runtime and platform matrix explicit without
  changing the current product boundary.
- Gaps: actual runtime proof remains in follow-on execution tracks.
