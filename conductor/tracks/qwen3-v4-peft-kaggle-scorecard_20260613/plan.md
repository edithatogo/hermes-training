# Plan: Qwen3 V4 PEFT Kaggle Scorecard

## Phase 1 - Kernel Spec

- [x] Task: Add a Kaggle runner for the public PEFT adapter scorecard.
- [x] Task: Add a guarded submitter that dry-runs by default.
- [x] Task: Stage `kernel-metadata.json`, run config, and runner code.
- [x] Task: Capture the dry-run command and artifact report.

## Phase 2 - Execute

- [x] Task: Verify the local Kaggle CLI is installed.
- [x] Task: Record the live Kaggle authentication blocker.
- [x] Task: Authenticate the Kaggle CLI.
- [x] Task: Resolve Kaggle quota visibility.
- [x] Task: Confirm public-input notebook execution contract.
- [x] Task: Add fail-closed local result artifact ingest gate.
- [x] Task: Submit the no-limit kernel only after explicit confirmation.
- [x] Task: Download result artifacts and update benchmark coverage if complete.
- [x] Task: Prepare a rerun path that avoids Kaggle P100/PyTorch `sm_60`
  incompatibility, or route the scorecard to Modal/Azure instead.
- [x] Task: Record CPython 3.12 Linux wheel proof for the pinned
  `p100-cu118` torch policy.
- [x] Task: Submit the P100-compatible rerun only after explicit approval.
- [x] Task: Recover SSD artifacts from Kaggle kernel version 2 and run the
  no-pending ingest gate.
- [x] Task: Validate the fixed P100-safe Kaggle runner contract before any
  further explicit rerun approval.
- [x] Task: Recover SSD artifacts from Kaggle kernel version 3 and run the
  no-pending ingest gate.
- [x] Task: Validate the NumPy-pinned P100 Kaggle runner contract before any
  further explicit rerun approval.
- [x] Task: Record existing Kaggle kernel version 4 submission and live status
  without claiming benchmark coverage.
- [x] Task: Recover SSD artifacts from Kaggle kernel version 4 after
  completion and run the no-pending ingest gate.
- [x] Task: Change the Kaggle runner/runtime strategy before any further rerun.
- [x] Task: Record existing Kaggle kernel version 5 submission and live status
  without claiming benchmark coverage.
- [x] Task: Recover SSD artifacts from Kaggle kernel version 5 after
  completion and run the no-pending ingest gate.
- [ ] Task: Route the scorecard to a different backend, or replace the Kaggle
  model-loading strategy before any further rerun.

## Health Check

- Target: >= 9.0 / 10
- Current estimate: 9.6 / 10 as a live-tested but blocked backend track.
- Evidence: `scripts/submit_kaggle_peft_scorecard.py` generated
  `reports/cloud/qwen3-v4-peft-kaggle-submit-dry-run-20260613.json` and staged
  the kernel folder under `reports/cloud/kaggle-qwen3-v4-peft-scorecard-20260613`.
  The 2026-06-13 browser-assisted OAuth flow completed and the CLI reports the
  local account as `edithatogo`; the guarded submitter dry-run now records no
  auth blocker. The public `kaggle quota` command still has a renderer/parser
  failure, but the same authenticated SDK endpoint returned GPU quota
  `108000s` total / `0s` used and TPU quota `72000s` total / `0s` used, with
  refresh at `2026-06-20T00:00:00Z`. The staged notebook contract passed in
  `reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.md`: public inputs
  only, no private data upload, GPU script metadata, no `--limit`, 21600s
  timeout, and explicit `--execute --confirm-kaggle-run` operator boundary.
  The no-limit GPU kernel was submitted as Kaggle version 1 on 2026-06-14; the
  live submit report is
  `reports/cloud/qwen3-v4-peft-kaggle-submit-live-20260614.json`. Kaggle
  completed, artifacts were downloaded to
  `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260614`,
  and the no-pending ingest gate failed in
  `reports/cloud/qwen3-v4-peft-kaggle-result-ingest-live-20260614.md` because
  lm-eval returned `1` before scoring. The concrete blocker is a Kaggle Tesla
  P100 (`sm_60`) assigned under a PyTorch CUDA build that supports `sm_70+`.
- Gaps: No scored Kaggle result exists. A retry must avoid P100, pin a
  compatible PyTorch/CUDA stack, use CPU fallback if acceptable, or route the
  scorecard to another persistent backend. The staged rerun path now pins a
  `p100-cu118` PyTorch policy, disables 4-bit/bitsandbytes for the P100 path,
  records wheel availability in
  `reports/cloud/kaggle-p100-torch-policy-wheel-proof-20260614.md`, and keeps
  execution gated behind `--execute --confirm-kaggle-run`. The
  P100-compatible rerun was submitted as Kaggle kernel version 2; evidence is
  tracked in `reports/cloud/qwen3-v4-peft-kaggle-submit-rerun-p100-20260614.json`.
  The kernel completed, and artifacts were recovered to
  `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v2`,
  but the no-pending ingest gate failed because lm-eval returned 1 with no
  result files after the runner fell back to 4-bit and the runtime ended on
  `torch=2.12.0+cu130`. The staged runner has since been hardened to default to
  no 4-bit and apply the P100 torch policy after dependencies; the contract
  validator now proves those guardrails. Kaggle kernel version 3 completed and
  artifacts were recovered to
  `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v3`,
  but the no-pending ingest gate failed because lm-eval returned 1 with no
  result files after Torch warned about NumPy 2 and transformers could not
  resolve `Qwen3ForCausalLM`. The staged runner now pins `numpy<2`, and the
  contract validator proves the no-4-bit default, final P100 torch policy, and
  NumPy pin. Kernel version 4 completed and artifacts were recovered to
  `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v4-20260614`.
  The no-pending ingest gate failed in
  `reports/cloud/qwen3-v4-peft-kaggle-result-ingest-rerun-p100-v4-20260614.md`
  because lm-eval returned 1 with no result files after `transformers==5.3.0`
  disabled PyTorch under `torch=2.2.2+cu118`; the P100 path now needs a
  runner/runtime change or a different backend. The staged runner now pins
  `transformers==4.57.6` plus `tokenizers==0.22.2`, and the contract validator
  proves that Qwen3 class support remains available while keeping Torch 2.2
  compatibility. Kernel version 5 was submitted from that staged runner and is
  now complete. Artifacts were recovered to
  `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v5-20260614`;
  the no-pending ingest gate failed in
  `reports/cloud/qwen3-v4-peft-kaggle-result-ingest-rerun-p100-v5-20260614.md`
  because `transformers==4.57.6` still could not resolve `Qwen3ForCausalLM` in
  the Kaggle runtime.
- Decision: keep Kaggle blocked and non-promotional; do not submit another
  unchanged P100/CUDA Kaggle rerun.
