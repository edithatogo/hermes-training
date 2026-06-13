# Specification: Cloud Modal Lightning Preflight

## Overview

The Hermes scorecard offload plan already records Colab, HF Jobs, Azure, NGC,
and Kaggle as gated execution backends. Modal and Lightning are plausible
additional zero-cost or student-credit-adjacent routes for wider edge/local
model scorecards, but they must be represented as blocked until authentication,
credits, GPU policy, and artifact recovery are proven.

## Goals

- Add Modal to the cloud backend preflight registry as a container/serverless candidate.
- Add Lightning to the cloud backend preflight registry as a Studio/job candidate.
- Add both backends to the fail-closed unblock checklist.
- Record local machine status without submitting jobs, using paid compute, or uploading artifacts.

## Acceptance Criteria

- Modal preflight reports `blocked-needs-auth` when the CLI exists but no token is configured.
- Lightning preflight reports `blocked-needs-teamspace-owner` when the CLI exists but no teamspace owner is configured.
- The unblock checklist lists operator-only commands and no execution submitter for either backend.
- Cloud blocker reports validate.

## Out Of Scope

- Running `modal token new` or `lightning login`.
- Creating Modal or Lightning submitters.
- Running remote scorecards.
- Uploading model artifacts or datasets.
