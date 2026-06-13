# Specification: Free Container Probe Readiness Validator

## Overview

The free-container account probe captures Modal, Kaggle, and Lightning account
state without launching jobs or using paid compute. Because that report records
auth-adjacent state and execution boundaries, readiness should validate that it
continues to include the required sections, no-job/no-paid-compute statement,
and no obvious secret strings.

## Goals

- Add a validator for `reports/cloud/free-container-account-probe-20260613.md`.
- Require Modal, Kaggle, Lightning, and current-decision sections.
- Require the no-job/no-resource/no-upload/no-paid-compute boundary.
- Reject obvious secret strings and remote execution commands.
- Wire the validator into `scripts/validate_readiness.py`.

## Acceptance Criteria

- The validator passes for the tracked report.
- Unit tests cover the passing path and failure for missing boundary/secret text.
- Full readiness includes the new validator.
- No cloud jobs or auth flows are run.

## Out Of Scope

- Re-running Modal, Kaggle, or Lightning probes.
- Changing backend statuses.
- Adding submitters.
