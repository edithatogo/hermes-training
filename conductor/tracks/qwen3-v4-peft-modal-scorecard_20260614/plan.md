# Plan: Qwen3 v4 PEFT Modal Scorecard

## Phase 1 - Modal App

- [x] Task: Add `scripts/modal_peft_lm_eval_selected.py`.
  - [x] Define a Modal app and T4 function.
  - [x] Install lm-eval/Transformers/PEFT dependencies in the Modal image.
  - [x] Download the public PEFT adapter inside the remote function.
  - [x] Write summary and lm-eval outputs under a Modal volume.

## Phase 2 - Guarded Submitter

- [x] Task: Add `scripts/submit_modal_peft_scorecard.py`.
  - [x] Dry-run by default.
  - [x] Require `--confirm-modal-run` with `--execute`.
  - [x] Require `--confirm-zero-cost-compute` with `--execute`.
  - [x] Record the exact Modal command without running it.

## Phase 3 - Evidence

- [x] Task: Generate `reports/cloud/qwen3-v4-peft-modal-submit-dry-run-20260614.json`.
- [x] Task: Add Modal submitter unit tests.
- [x] Task: Add fail-closed Modal scorecard execution contract.
- [x] Task: Add fail-closed Modal result ingest gate.
- [x] Task: Defer free credit/grant or zero-cost GPU policy confirmation until
  Modal is explicitly selected for cross-provider comparison.
  - [x] Current-month billing probe returned no usage rows in
    `reports/cloud/modal-billing-this-month-20260614.md`.
  - [x] Fail-closed policy gate added at
    `reports/cloud/modal-policy-gate-20260614.md`; it records
    `execution_allowed=false` because empty billing is not zero-cost proof.
  - [x] Non-secret evidence template added at
    `reports/cloud/modal-policy-evidence-template-20260614.md`; copy it to
    `reports/cloud/modal-policy-evidence-20260614.json` only after free credit,
    grant, or paid-compute approval is confirmed.
  - [x] Record that execution still needs free GPU credit/grant policy or
    explicit paid-compute approval.
- [x] Task: Defer Modal scorecard submission; keep execution guarded behind
  explicit approval and zero-cost/paid-compute confirmation.
- [x] Task: Defer local result JSON and Modal volume artifact recovery; use
  Kaggle v7 artifacts for current benchmark coverage.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10 as a prepared/deferred backend track with current
  benchmark coverage supplied by Kaggle v7.
- Evidence: The Modal app and submitter are present, and the dry-run report
  records no blockers while `execute` and both confirmations are false. The
  dry-run also records that the Modal policy gate is observed. Modal CLI is
  authenticated to workspace `d-a-mordaunt`, and the current-month billing
  report is empty. The fail-closed policy gate is tracked at
  `reports/cloud/modal-policy-gate-20260614.md`, the non-secret evidence
  template is tracked at
  `reports/cloud/modal-policy-evidence-template-20260614.md`, the Modal execution contract is tracked at
  `reports/cloud/qwen3-v4-peft-modal-contract-20260614.md`, and the pending
  Modal result-ingest gate is tracked at
  `reports/cloud/qwen3-v4-peft-modal-result-ingest-20260614.md`.
- Gaps: Free credit/grant and GPU policy are not proven; no Modal job was run.
  This is no longer a blocker for the current selected-task scorecard because
  Kaggle kernel version 7 completed all five no-limit tasks and passed the
  no-pending ingest gate.
- Decision: close Modal as a guarded fallback. Do not launch Modal GPU work
  unless zero-cost/paid-compute evidence and explicit run approval are
  recorded for a cross-provider comparison.
