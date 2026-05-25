# Plan: Qwen3 V4 Release Evidence And Publication Gate

## Phase 1 - Publication Gate Validator

- [x] Task: Add a machine-checkable publication bundle validator.
    - [x] Parse markdown checklist items from a publication folder.
    - [x] Require core evidence files for the Qwen3 v4 bundle.
    - [x] Treat missing non-quality release gates as blocked, not as failures.
    - [x] Add `--require-ready` for future use when public release is requested.
- [x] Task: Add tests for the validator.
    - [x] Cover a blocked checklist with required blockers.
    - [x] Cover a ready checklist with all release gates complete.
    - [x] Cover missing required files.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Gate Validator' (Protocol in workflow.md)

## Phase 2 - Qwen3 V4 Release Decision Bundle

- [x] Task: Record the release decision.
    - [x] Summarize approved GitHub evidence.
    - [x] Summarize private Hugging Face draft status.
    - [x] Preserve public release blockers.
    - [x] Link exact raw output paths and commands.
- [x] Task: Update the publish-readiness checklist.
    - [x] Add machine gate status.
    - [x] Add the validator command.
    - [x] Keep public publication blocked pending human approval and redistribution review.
- [x] Task: Conductor - Automated Review and Checkpoint 'Qwen3 V4 Release Decision Bundle' (Protocol in workflow.md)

## Phase 3 - Validation And Closeout

- [x] Task: Run validation.
    - [x] `git diff --check`
    - [x] `python3 -m unittest discover -s tests`
    - [x] `./.venv/bin/python scripts/validate_readiness.py`
    - [x] Qwen3 v4 publication validator command.
- [x] Task: Update registry and track health.
    - [x] Mark this track complete only if health remains `>= 9.5`.
    - [x] Record any remaining blockers as explicit release blockers, not task blockers.
- [x] Task: Conductor - Automated Review and Checkpoint 'Validation And Closeout' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Rationale: the strict local quality gate and private draft upload are already
  proven; this track improves release governance and fail-closed checks without
  changing model artifacts.
- Remaining blockers: public release still requires redistribution review,
  standard benchmark positioning, finalized model card, and human approval.
