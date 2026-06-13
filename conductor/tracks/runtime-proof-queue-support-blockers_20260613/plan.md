# Plan: Runtime Proof Queue Support Blockers

## Phase 1 - Queue Classification

- [x] Task: Add a distinct runtime-support lane.
  - [x] Detect candidates blocked by current local runtime support.
  - [x] Route them to `runtime-support-upgrade`.
  - [x] Keep prompt-profile repair blockers ahead of runtime-support classification.

## Phase 2 - Action Guidance

- [x] Task: Avoid repeat proof commands for known unsupported runtimes.
  - [x] Emit a command card that verifies updated runtime/converter support first.
  - [x] Add rendered policy guidance for retry conditions.
  - [x] Keep immediate proof candidates ahead of runtime-support-upgrade candidates.

## Phase 3 - Tests And Reports

- [x] Task: Add focused unit coverage.
  - [x] Verify lane classification.
  - [x] Verify command wording avoids `run_local_pilot_benchmark.py`.
  - [x] Verify priority order.
- [x] Task: Regenerate the runtime proof action queue.
  - [x] Update JSON coverage output.
  - [x] Update Markdown queue output.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: The regenerated queue now separates 9 known runtime-support blockers from the immediate Mac runtime proof lane.
- Validation: Focused queue tests, runtime proof queue validation, Conductor track consistency, and hub readiness validation are required before commit.
- Gaps: Runtime upgrades themselves remain future work and should be handled only after a concrete runtime/converter change exists.
- Decision: Complete. The track improves prioritization without making new runtime performance claims.
