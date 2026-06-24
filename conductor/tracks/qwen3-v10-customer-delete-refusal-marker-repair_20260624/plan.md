# Plan: Qwen3 v10 Customer-Delete Refusal-Marker Repair

## Phase 1 - Dataset And Config

- [x] Task: Add v10 customer-delete repair data.
    - [x] Add materializer for customer-delete-only refusal-marker rows.
    - [x] Materialize `expanded_splits_v10_customer_delete_refusal_marker_repair`.
    - [x] Add validator and unit tests.
- [x] Task: Add bounded v10 training config.
    - [x] Use Qwen3 4B MLX base.
    - [x] Write to a new v10 adapter path.
    - [x] Preserve the full140 training envelope.
- [x] Task: Conductor - User Manual Verification 'Phase 1 - Dataset And Config' (Protocol in workflow.md)

## Phase 2 - Train And Rerun

- [x] Task: Train bounded v10 adapter.
    - [x] Log stdout/stderr under `/Volumes/PortableSSD/hermes-evals/training/qwen3-v10-customer-delete-refusal-marker-repair-20260624`.
    - [x] Trained `140` iterations, `32941` tokens, final validation loss `0.669`, peak memory `3.770 GB`.
- [x] Task: Rerun pinned safety/refusal suite.
    - [x] Use model `Qwen/Qwen3-4B-MLX-4bit`.
    - [x] Use v10 adapter.
    - [x] Use user prefix `/no_think`.
    - [x] Use assistant prefill `<think>\n\n</think>\n\n`.
    - [x] Write outputs to `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v10-customer-delete-refusal-marker-repair-20260624`.
    - [x] Gate result: strict pass `0.750`, JSON validity `1.000`, argument accuracy `0.667`, empty-think prefix cases `0`, residual failures `2`, refusal-marker echoes `1`, text-mode tool-call rows `0`.
- [x] Task: Conductor - User Manual Verification 'Phase 2 - Train And Rerun' (Protocol in workflow.md)
    - [x] Remaining blocker: v10 still echoes `delete_customer_record` and regresses lab-order argument correctness.

## Phase 3 - Report, Validate, Push

- [x] Task: Add v10 run report, validator, and tests.
    - [x] Record strict pass, JSON validity, argument accuracy, empty-think count, residual failures, marker echoes, text-mode tool calls, and publication boundary.
    - [x] Wire validator into readiness.
- [x] Task: Add runtime refusal-marker normalization proof after v10 failed gates.
    - [x] Normalize only the single saved v9 text-mode response that echoed `delete_customer_record`.
    - [x] Rescore normalized v9 responses on the pinned safety/refusal suite.
    - [x] Record runtime-normalized strict pass `1.000`, JSON validity `1.000`, argument accuracy `1.000`, empty-think prefix cases `0`, residual failures `0`, and changed responses `1`.
    - [x] Wire runtime proof validator into readiness.
- [x] Task: Run focused checks and readiness.
- [x] Task: Commit/push nested `gemma4` if dirty, then hub root.
- [x] Task: Upload private HF evidence-only artifact if v10 produces new run evidence.
    - [x] Uploaded private evidence-only artifact to `edithatogo/hermes-training-artifacts` at revision `1d93c2af90949b5c846bf7383f3f04b9c55a083c`.
    - [x] Confirmed no model weights, adapter weights, or checkpoints were included.
- [x] Task: Conductor - User Manual Verification 'Phase 3 - Report, Validate, Push' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10.
- Current estimate: 9.6 / 10.
- Current blocker: none for the v10 decision. v10 trained and reran, failed the
  target gates, and regressed from v9 full140, so the correct outcome is
  rejection rather than further promotion. Do not publish v10 weights. The
  selected runtime-side safety/refusal path is the v9 normalized profile; raw
  model promotion remains blocked until a raw run passes without normalization.
