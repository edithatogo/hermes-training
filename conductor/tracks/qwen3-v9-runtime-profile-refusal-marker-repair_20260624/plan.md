# Plan: Qwen3 v9 Runtime-Profile Refusal Marker Repair

## Phase 1 - Runtime-Profile Blocker Split

- [x] Task: Run an assistant-prefill-only profile smoke against the v8 adapter.
    - [x] Confirm empty-think prefix cases improve from `8` to `0`.
    - [x] Confirm tool-call JSON validity and argument correctness remain `1.000`.
    - [x] Confirm residual strict failures remain refusal-marker echoes.
- [x] Task: Run a stronger refusal-prefix smoke only as a bounded negative control.
    - [x] Confirm it regresses behavior and is not a viable repair path.
- [x] Task: Record repo evidence and keep raw outputs on `/Volumes/PortableSSD`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Runtime-Profile Blocker Split' (Protocol in workflow.md)

## Phase 2 - Residual Refusal Repair Data

- [ ] Task: Generate v9 refusal-only repair rows for the two residual IDs.
    - [ ] Use generic refusal text that does not echo unavailable tool names.
    - [ ] Avoid changing passing tool-call rows unless validation shows leakage.
- [ ] Task: Add validation for forbidden markers and text-mode refusal shape.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Residual Refusal Repair Data' (Protocol in workflow.md)

## Phase 3 - Bounded Rerun And Gate Decision

- [ ] Task: Train or run the smallest bounded v9 repair experiment.
- [ ] Task: Rerun the pinned 8-case safety/refusal suite with assistant prefill.
- [ ] Task: Record strict pass, wrapper count, residual failures, and publication boundary.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Bounded Rerun And Gate Decision' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10 before marking complete.
- Current estimate: 7.2 / 10.
- Current blocker: residual refusal marker echoes remain in two cases after the
  wrapper blocker is cleared by assistant prefill.
