# Plan: Prompt/Profile Repair Ledger And Selection

## Phase 1 - Executability Guard

- [x] Task: Exclude cloud-only candidates from executable local experiments.
  - [x] Keep non-local rows visible through the ledger.
  - [x] Prevent Mac-local commands for Azure/offload rows.

## Phase 2 - Ledger

- [x] Task: Build the execution ledger.
  - [x] Record pending-local, pending-endpoint, pending-local-with-analysis, and
    blocked-non-local statuses.
  - [x] Keep result fields blank until a real run exists.
  - [x] Record promotion gates for every row.

## Phase 3 - Validation

- [x] Task: Add focused unit tests.
- [x] Task: Add deterministic ledger validation and readiness wiring.
- [x] Task: Regenerate experiment, ledger, and selection reports.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: The ledger prevents non-local rows from being mistaken for Mac-local
  work and gives a clear one-at-a-time execution boundary.
- Validation: Focused tests, ledger/selection validators, Conductor consistency,
  and full readiness are required before commit.
- Gaps: No repair experiment was executed.
- Decision: Complete. The next local run should be chosen from a pending-local
  ledger row.
