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
- [ ] Task: Confirm free credit/grant or zero-cost GPU policy.
  - [x] Current-month billing probe returned no usage rows in
    `reports/cloud/modal-billing-this-month-20260614.md`.
  - [x] Fail-closed policy gate added at
    `reports/cloud/modal-policy-gate-20260614.md`; it records
    `execution_allowed=false` because empty billing is not zero-cost proof.
  - [ ] Still need free GPU credit/grant policy or explicit paid-compute
    approval before execution.
- [ ] Task: Submit the Modal scorecard only after explicit approval.
- [ ] Task: Recover local result JSON and Modal volume artifacts if complete.

## Health Check

- Target: >= 9.0 / 10
- Current estimate: 9.3 / 10 as a prepared-but-policy-gated backend track.
- Evidence: The Modal app and submitter are present, and the dry-run report
  records no blockers while `execute` and both confirmations are false. The
  dry-run also records that the Modal policy gate is observed. Modal CLI is
  authenticated to workspace `d-a-mordaunt`, and the current-month billing
  report is empty. The fail-closed policy gate is tracked at
  `reports/cloud/modal-policy-gate-20260614.md`, the Modal execution contract is tracked at
  `reports/cloud/qwen3-v4-peft-modal-contract-20260614.md`, and the pending
  Modal result-ingest gate is tracked at
  `reports/cloud/qwen3-v4-peft-modal-result-ingest-20260614.md`.
- Gaps: Free credit/grant and GPU policy are not proven; no Modal job was run.
- Decision: Keep Modal blocked until zero-cost compute and explicit run approval
  are confirmed.
