# Plan: Cloud Blocker Artifact-Aware Kaggle Status

## Phase 1 - Generator Update

- [x] Task: Add optional Kaggle contract and ingest report inputs to the cloud unblock checklist generator.
- [x] Task: Derive `prepared-needs-run-approval` when the notebook contract passes and ingest gate is ready.
- [x] Task: Regenerate the backend unblock checklist and active blocked-track matrix.

## Phase 2 - Validation

- [x] Task: Add unit coverage for the artifact-derived Kaggle run-approval status.
- [x] Task: Require the Modal scorecard track in cloud blocker report validation.
- [x] Task: Run focused cloud report tests and full readiness.

## Health Check

- Target: >= 9.8 / 10
- Current estimate: 9.8 / 10
- Evidence:
  - `tests/test_build_cloud_unblock_checklist.py` covers the derived Kaggle status.
  - `scripts/validate_cloud_blocker_reports.py` now requires the Modal blocked track.
  - `reports/cloud/active-blocked-track-matrix-20260613.md` shows Kaggle blocked on run approval and artifact recovery.
- Remaining blocker: explicit live execution approval remains external.
