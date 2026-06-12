# Roadmap Regression and Publication Gate Plan

## Phase 1: Consistency Contract

- [x] Task: Define the source-of-truth hierarchy.
    - [x] Treat benchmark reports as execution evidence.
    - [x] Treat `MODEL_CANDIDATES.yaml` as structured candidate state.
    - [x] Treat `FUTURE_MODELS.md` as roadmap synthesis.
    - [x] Treat `HANDOFF.md` as the next-action operator summary.
- [x] Task: Identify consistency checks.
    - [x] List required fields for promoted, blocked, rejected, and watchlist candidates.
    - [x] Identify stale scan-report conclusions that require follow-up notes rather than deletion.
- [x] Task: Conductor - User Manual Verification 'Consistency Contract' (Protocol in workflow.md)

Evidence: `reports/publication/roadmap-regression-publication-gate-20260612.md` defines the source-of-truth hierarchy and the rule that stale or failed scan/runtime conclusions are annotated, not deleted.

## Phase 2: Automated and Manual Regression Checks

- [x] Task: Run repo validation.
    - [x] Run `source scripts/env.sh && ./.venv/bin/python scripts/validate_readiness.py`.
    - [x] Run model-candidate consistency checks.
    - [x] Run targeted report or YAML checks when roadmap artifacts change.
- [x] Task: Inspect publication-sensitive paths.
    - [x] Confirm private data, secrets, and large generated artifacts remain untracked.
    - [x] Confirm public claims cite concrete benchmark evidence.
- [x] Task: Conductor - User Manual Verification 'Automated and Manual Regression Checks' (Protocol in workflow.md)

Evidence: readiness and `scripts/check_model_candidates.py` passed on 2026-06-12. The report records the current dirty-worktree boundary so mem0/frontier in-progress changes are not co-committed accidentally.

## Phase 3: Publication Gate Audit

- [x] Task: Audit model and dataset publication readiness.
    - [x] Separate GitHub code publication from Hugging Face model/dataset publication.
    - [x] Confirm license and source redistribution status before any public upload.
    - [x] Require explicit approval for public model or dataset artifacts.
- [x] Task: Audit cloud execution provenance.
    - [x] Record Colab, Azure, NGC, or Kaggle provenance for benchmark results.
    - [x] Keep cloud-only findings from being misread as local compatibility proof.
- [x] Task: Conductor - User Manual Verification 'Publication Gate Audit' (Protocol in workflow.md)

Evidence: the publication report keeps GitHub docs/code publication separate from Hugging Face artifacts and records provider-specific provenance rules for Colab, Azure, NGC, and Kaggle.

## Phase 4: Final Reconciliation and Push

- [x] Task: Update operator-facing docs.
    - [x] Update `FUTURE_MODELS.md`.
    - [x] Update `MODEL_CANDIDATES.yaml`.
    - [x] Update `HANDOFF.md`.
    - [x] Update relevant scan follow-up reports.
- [x] Task: Validate, commit, and push.
    - [x] Run readiness and candidate checks.
    - [x] Commit only reviewed changes.
    - [x] Push to the remote GitHub repo.
- [x] Task: Conductor - User Manual Verification 'Final Reconciliation and Push' (Protocol in workflow.md)

Evidence: `FUTURE_MODELS.md` and root `MODEL_CANDIDATES.yaml` already matched the current 2026-06-12 scan set and did not require direct edits in this gate. `HANDOFF.md` and the new publication report were updated. Final commit/push evidence is recorded in Git history for this track.
