# Plan: Qwen3 V4 PEFT NGC Cloud Function Scorecard

## Phase 1 - Discovery

- [x] Task: Inspect the installed NGC CLI top-level command surface.
- [x] Task: Confirm `ngc batch` is not available in this installation.
- [x] Task: Inspect Cloud Function task/function/GPU command surfaces.
- [x] Task: Record current NGC config state without secrets.

## Phase 2 - Execution Gate

- [x] Task: Record the likely `ngc cloud-function task create` route.
- [x] Task: Record required auth, org/team, GPU quota, container image, and
  result persistence blockers.
- [x] Task: Defer NGC auth until the user supplies keys or completes
  SSO.
- [x] Task: Defer org/team, GPU quota, and registry access verification until
  NGC is explicitly selected for cross-provider comparison.
- [x] Task: Defer benchmark container image build/selection; keep the tracked
  Containerfile as the reproducible recipe.
- [x] Task: Defer bounded NGC task submission; keep execution gated behind
  explicit confirmation and entitlement proof.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10 as a completed discovery/guarded fallback track
  with current benchmark coverage supplied by Kaggle v7.
- Evidence: `reports/cloud/qwen3-v4-peft-ngc-cloud-function-discovery-20260613.md`
  records the observed CLI surface and blockers.
  `scripts/submit_ngc_cloud_function_scorecard.py` now builds the guarded
  Cloud Function task command and fails closed while auth, entitlement, GPU
  quota, and a real NGC registry container image are absent.
  `templates/ngc/qwen3-v4-peft-scorecard.Containerfile` prepares the benchmark
  container recipe, but no NGC registry image has been built, pushed, or
  selected yet.
- Gaps: no NGC auth, no org/team, no GPU quota, no benchmark container, and no
  result persistence proof. This is no longer a blocker for the current
  selected-task scorecard because Kaggle kernel version 7 completed all five
  no-limit tasks and passed the no-pending ingest gate.
- Decision: close NGC as a guarded discovery track. Do not configure NGC auth,
  push containers, or submit tasks unless credentials/entitlements are provided
  and NGC is explicitly chosen for cross-provider comparison.
