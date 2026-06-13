# Plan: Cloud Modal Lightning Preflight

## Phase 1 - Backend Preflight

- [x] Task: Add Modal preflight summary.
  - [x] Check CLI version.
  - [x] Check profile list.
  - [x] Check token info.
  - [x] Fail closed until auth and credit policy are proven.

- [x] Task: Add Lightning preflight summary.
  - [x] Check CLI version.
  - [x] Check Studio list.
  - [x] Check machine list.
  - [x] Fail closed until login, teamspace, credits, machine type, and artifact recovery are proven.

## Phase 2 - Unblock Checklist

- [x] Task: Add Modal operator actions.
- [x] Task: Add Lightning operator actions.
- [x] Task: Keep the checklist non-executing.

## Phase 3 - Reports And Validation

- [x] Task: Regenerate cloud backend preflight report.
- [x] Task: Regenerate cloud backend unblock checklist.
- [x] Task: Validate cloud blocker reports.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: Modal and Lightning are visible in the backend registry and remain blocked until non-secret account, credit, and artifact contracts are proven.
- Validation: Cloud preflight tests, cloud blocker validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: No authenticated Modal or Lightning job was run.
- Decision: Complete. The plan has more offload options without weakening cost/auth gates.
