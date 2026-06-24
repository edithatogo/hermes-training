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
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Residual Refusal Repair Data' (Protocol in workflow.md)

## Phase 3 - Bounded Rerun And Gate Decision

- [x] Task: Train or run the smallest bounded v9 repair experiment.
    - [x] Trained `80` iterations from `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v9-runtime-profile-refusal-marker-repair.yaml`.
    - [x] Training log: `/Volumes/PortableSSD/hermes-evals/training/qwen3-v9-runtime-profile-refusal-marker-repair-20260624/stdout.log`.
- [x] Task: Rerun the pinned 8-case safety/refusal suite with assistant prefill.
    - [x] Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v9-runtime-profile-refusal-marker-repair-20260624`.
    - [x] Runtime profile: user prefix `/no_think\n`, assistant prefill `<think>\n\n</think>\n\n`.
- [x] Task: Record strict pass, wrapper count, residual failures, and publication boundary.
    - [x] Report: `reports/benchmark/official-candidates/qwen3-v9-runtime-profile-refusal-marker-repair-run-20260624.md`.
    - [x] Gate result: strict pass `0.125`, empty-think prefix cases `0`, residual failures `7`, refusal-marker echoes `4`, text-mode tool-call rows `1`.
    - [x] Publication boundary: private evidence-only; do not publish v9 weights.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Bounded Rerun And Gate Decision' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10 before marking complete.
- Current estimate: 8.1 / 10.
- Current blocker: the bounded v9 train and pinned rerun completed, but v9
  regressed strict pass from the v8 runtime-profile source (`0.750` to `0.125`)
  while leaving `7` residual failures, `4` refusal-marker echoes, and `1`
  text-mode tool-call row. Keep v9 as evidence-only and do not publish weights.
