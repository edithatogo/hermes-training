# Plan: Qwen3 V4 PEFT HF Jobs Scorecard

## Phase 1 - Artifact

- [x] Task: Create a separate public PEFT-converted adapter repo.
- [x] Task: Upload metadata and converted adapter weights.
- [x] Task: Verify remote files and visibility.

## Phase 2 - Job Spec

- [x] Task: Add an HF Jobs no-limit config using a mounted adapter path.
- [x] Task: Record hardware/cost options and candidate command.
- [x] Task: Add a self-contained UV or Docker job payload that embeds the
  harness script and persists outputs to Hub storage.
- [x] Task: Add a guarded submitter that dry-runs by default and requires
  explicit paid-compute confirmation before invoking `hf jobs run`.

## Phase 3 - Execute

- [x] Task: Attempt a minimal persistent HF Jobs route submission.
- [x] Task: Record the live HF Jobs credit blocker.
- [x] Task: Defer job submission because HF Jobs returned `402 Payment
  Required` and Kaggle v7 supplied the validated no-limit selected-task
  scorecard evidence.
- [x] Task: Keep result artifact recovery instructions documented for a future
  HF Jobs rerun after credits/grant capacity is available.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10 as a prepared/deferred backend track with current
  benchmark coverage supplied by Kaggle v7.
- Evidence: HF CLI is authenticated as `edithatogo`; HF Jobs hardware is
  available; PEFT adapter is now publicly mounted from the Hub; a Docker job
  payload can upload results to a Hub dataset; the guarded submitter generated
  `reports/cloud/qwen3-v4-peft-hf-jobs-submit-dry-run-20260613.json`.
- Gaps: live HF Jobs submission returned `402 Payment Required` because the
  prepaid credit balance is insufficient; no job ID was created and artifact
  persistence has not yet been live-tested. This is no longer a blocker for the
  current selected-task scorecard because Kaggle kernel version 7 completed all
  five no-limit tasks and passed the no-pending ingest gate.
- Decision: close HF Jobs as a prepared, credit-gated fallback route. Do not
  submit HF Jobs unless credits/grant capacity becomes available and a
  cross-provider comparison is explicitly needed.
