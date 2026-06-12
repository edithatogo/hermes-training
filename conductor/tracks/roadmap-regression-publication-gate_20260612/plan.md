# Roadmap Regression and Publication Gate Plan

## Phase 1: Consistency Contract

- [ ] Task: Define the source-of-truth hierarchy.
    - [ ] Treat benchmark reports as execution evidence.
    - [ ] Treat `MODEL_CANDIDATES.yaml` as structured candidate state.
    - [ ] Treat `FUTURE_MODELS.md` as roadmap synthesis.
    - [ ] Treat `HANDOFF.md` as the next-action operator summary.
- [ ] Task: Identify consistency checks.
    - [ ] List required fields for promoted, blocked, rejected, and watchlist candidates.
    - [ ] Identify stale scan-report conclusions that require follow-up notes rather than deletion.
- [ ] Task: Conductor - User Manual Verification 'Consistency Contract' (Protocol in workflow.md)

## Phase 2: Automated and Manual Regression Checks

- [ ] Task: Run repo validation.
    - [ ] Run `source scripts/env.sh && ./.venv/bin/python scripts/validate_readiness.py`.
    - [ ] Run model-candidate consistency checks.
    - [ ] Run targeted report or YAML checks when roadmap artifacts change.
- [ ] Task: Inspect publication-sensitive paths.
    - [ ] Confirm private data, secrets, and large generated artifacts remain untracked.
    - [ ] Confirm public claims cite concrete benchmark evidence.
- [ ] Task: Conductor - User Manual Verification 'Automated and Manual Regression Checks' (Protocol in workflow.md)

## Phase 3: Publication Gate Audit

- [ ] Task: Audit model and dataset publication readiness.
    - [ ] Separate GitHub code publication from Hugging Face model/dataset publication.
    - [ ] Confirm license and source redistribution status before any public upload.
    - [ ] Require explicit approval for public model or dataset artifacts.
- [ ] Task: Audit cloud execution provenance.
    - [ ] Record Colab, Azure, NGC, or Kaggle provenance for benchmark results.
    - [ ] Keep cloud-only findings from being misread as local compatibility proof.
- [ ] Task: Conductor - User Manual Verification 'Publication Gate Audit' (Protocol in workflow.md)

## Phase 4: Final Reconciliation and Push

- [ ] Task: Update operator-facing docs.
    - [ ] Update `FUTURE_MODELS.md`.
    - [ ] Update `MODEL_CANDIDATES.yaml`.
    - [ ] Update `HANDOFF.md`.
    - [ ] Update relevant scan follow-up reports.
- [ ] Task: Validate, commit, and push.
    - [ ] Run readiness and candidate checks.
    - [ ] Commit only reviewed changes.
    - [ ] Push to the remote GitHub repo.
- [ ] Task: Conductor - User Manual Verification 'Final Reconciliation and Push' (Protocol in workflow.md)
