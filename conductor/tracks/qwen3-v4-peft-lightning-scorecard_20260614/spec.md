# Specification: Qwen3 v4 PEFT Lightning Scorecard

## Overview

Lightning Jobs is a potential persistent-backend fallback for the no-limit
Qwen3 v4 PEFT selected-task lm-eval scorecard. The local CLI is installed, but
the backend remains fail-closed until login, Teamspace ownership, machine
availability, zero-cost compute status, result persistence, and explicit run
approval are all proven.

## Goals

- Add a guarded Lightning Jobs submitter that dry-runs by default.
- Stage a no-limit PEFT scorecard configuration.
- Require explicit run and zero-cost-compute confirmations for execution.
- Keep the placeholder Teamspace fail-closed.
- Surface Lightning in the active blocked-track matrix.

## Acceptance Criteria

- The submitter emits a dry-run report without launching Lightning work.
- Execution requires `--execute --confirm-lightning-run --confirm-zero-cost-compute`.
- Execution with `<owner>/<teamspace>` remains blocked.
- Cloud blocker reports list the Lightning scorecard track and guarded commands.

## Out Of Scope

- Running Lightning login.
- Submitting a Lightning job.
- Treating any unproven free tier or credit state as authorization.
