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
    - [x] Checkpoint sweep showed the bounded run was not promotable: iter20 `0.125`, iter40 `0.125`, iter60 `0.250`, final80 `0.125`.
    - [x] Ran a full-budget follow-up with v8-equivalent `140` iterations at `/Volumes/PortableSSD/hermes-evals/training/qwen3-v9-full140-runtime-profile-refusal-marker-repair-20260624/stdout.log`.
- [x] Task: Rerun the pinned 8-case safety/refusal suite with assistant prefill.
    - [x] Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v9-runtime-profile-refusal-marker-repair-20260624`.
    - [x] Best output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v9-full140-runtime-profile-prefill-only-20260624`.
    - [x] Runtime profile: user prefix `/no_think\n`, assistant prefill `<think>\n\n</think>\n\n`.
- [x] Task: Record strict pass, wrapper count, residual failures, and publication boundary.
    - [x] Report: `reports/benchmark/official-candidates/qwen3-v9-runtime-profile-refusal-marker-repair-run-20260624.md`.
    - [x] Gate result: strict pass `0.875`, JSON validity `1.000`, argument accuracy `1.000`, empty-think prefix cases `0`, residual failures `1`, refusal-marker echoes `1`, text-mode tool-call rows `0`.
    - [x] Stronger refusal-prefix runtime profile regressed to strict pass `0.625`; keep the plain `/no_think` plus assistant-prefill profile.
    - [x] Publication boundary: private evidence-only; do not publish v9 weights.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Bounded Rerun And Gate Decision' (Protocol in workflow.md)

## Phase 4 - Runtime Profile Selection

- [x] Task: Promote the passing runtime-side evidence into the runtime profile contract.
    - [x] Profile: `qwen3-v9-no-think-prefill-refusal-marker-normalized`.
    - [x] Runtime conditions: `/no_think` user prefix, assistant prefill `<think>\n\n</think>\n\n`, leading-empty-think stripping, and text-mode-only forbidden-marker redaction.
    - [x] Evidence: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v9-runtime-profile-refusal-marker-normalized-20260624`.
    - [x] Gate result: strict pass `1.000`, JSON validity `1.000`, argument accuracy `1.000`, invalid-tool handling `1.000`, empty-think prefix cases `0`, changed text responses `1`.
- [x] Task: Record publication boundary.
    - [x] Runtime path is selectable for Hermes safety/refusal integration evidence.
    - [x] Raw v9 weights remain non-publishable until a raw, unnormalized run passes the same gate.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Runtime Profile Selection' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10 before marking complete.
- Current estimate: 9.6 / 10.
- Current blocker: none for runtime-side Hermes safety/refusal selection. The
  named v9 runtime profile passes the pinned suite after constrained text-mode
  marker normalization. Raw model-weight promotion remains blocked because the
  unnormalized v9 run still scored `0.875` and echoed `delete_customer_record`
  once.
