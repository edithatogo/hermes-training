# Spec: Cloud Blocker Artifact-Aware Kaggle Status

## Objective

Keep the cloud unblock checklist and active blocked-track matrix aligned with
tracked local evidence after supporting gates complete.

## Requirements

- Preserve the raw backend preflight status as account-state evidence.
- Derive the operator-facing Kaggle status from the passed notebook contract
  and staged result-ingest gate.
- Render Kaggle as blocked on explicit run approval and artifact recovery once
  those local gates are ready.
- Require the Modal scorecard track to appear in the active blocked-track
  matrix.
- Keep full readiness green.

## Non-Goals

- Submit Kaggle, Modal, or any other remote job.
- Change raw account preflight evidence.
- Mark externally blocked scorecard tracks complete.

## Health Target

Target health: 9.8 / 10.
