# Plan: Cloud Blocked Matrix Modal Lightning Mapping

## Phase 1 - Classifier

- [x] Task: Add Modal backend mapping.
- [x] Task: Add Lightning backend mapping.

## Phase 2 - Regression Coverage

- [x] Task: Add unit coverage for Modal and Lightning track classification.

## Phase 3 - Validation

- [x] Task: Run blocked-track matrix tests.
- [x] Task: Run cloud blocker report validation.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.9 / 10
- Evidence: Future blocked Modal/Lightning tracks will resolve to their checklist entries instead of `unknown`.
- Validation: Blocked-track matrix tests, cloud blocker validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: No Modal or Lightning execution track exists yet.
- Decision: Complete. This keeps the expanded offload plan internally consistent.
