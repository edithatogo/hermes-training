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

- [x] Task: Generate v9 refusal-only repair rows for the two residual IDs.
    - [x] Dataset: `gemma4/data/strict_tool_call/expanded_splits_v9_runtime_profile_refusal_marker_repair`.
    - [x] Config: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v9-runtime-profile-refusal-marker-repair.yaml`.
    - [x] Use generic refusal text that does not echo unavailable tool names.
    - [x] Avoid changing passing tool-call rows unless validation shows leakage.
- [x] Task: Add validation for forbidden markers and text-mode refusal shape.
    - [x] Validator: `scripts/validate_qwen3_v9_repair_dataset.py`.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Residual Refusal Repair Data' (Protocol in workflow.md)

## Phase 3 - Bounded Rerun And Gate Decision

- [ ] Task: Train or run the smallest bounded v9 repair experiment.
- [ ] Task: Rerun the pinned 8-case safety/refusal suite with assistant prefill.
- [ ] Task: Record strict pass, wrapper count, residual failures, and publication boundary.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Bounded Rerun And Gate Decision' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10 before marking complete.
- Current estimate: 8.2 / 10.
- Current blocker: v9 repair data and config are prepared, but the bounded train
  and pinned 8-case safety/refusal rerun have not yet been executed.
