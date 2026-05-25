# Plan: Qwen3 V4 Dataset Source Redistribution Review

## Phase 1 - Source Audit

- [x] Task: Add source provenance audit CLI.
    - [x] Summarize source classes.
    - [x] Detect unknown sources.
    - [x] Record no-think variants and duplicate ID counts.
- [x] Task: Add source audit tests.
    - [x] Cover missing source as strict seed.
    - [x] Cover unknown source blocking.
- [x] Task: Conductor - Automated Review and Checkpoint 'Source Audit' (Protocol in workflow.md)

## Phase 2 - Redistribution Review

- [x] Task: Generate Qwen3 v4 source audit JSON.
- [x] Task: Write redistribution review.
- [x] Task: Update release decision and publish-readiness checklist.
- [x] Task: Conductor - Automated Review and Checkpoint 'Redistribution Review' (Protocol in workflow.md)

## Phase 3 - Validation

- [x] Task: Run validation.
    - [x] `git diff --check`
    - [x] `python3 -m unittest discover -s tests`
    - [x] `./.venv/bin/python scripts/validate_readiness.py`
    - [x] Publication bundle validator remains blocked, not ready.
- [x] Task: Confirm health.
    - [x] Health remains `9.8 / 10`.
    - [x] Remaining blockers are release blockers, not implementation blockers.
- [x] Task: Conductor - Automated Review and Checkpoint 'Validation' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Remaining blockers: standard benchmark positioning, finalized model card, and
  human publication approval.
