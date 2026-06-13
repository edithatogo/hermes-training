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
- [ ] Task: Configure NGC auth only after the user supplies keys or completes
  SSO.
- [ ] Task: Verify org/team, GPU quota, and registry access.
- [ ] Task: Build or select a benchmark container image.
- [ ] Task: Submit a bounded NGC task only after explicit confirmation.

## Health Check

- Target: >= 8.5 / 10
- Current estimate: 7.8 / 10 as a discovery-only track.
- Evidence: `reports/cloud/qwen3-v4-peft-ngc-cloud-function-discovery-20260613.md`
  records the observed CLI surface and blockers.
  `scripts/submit_ngc_cloud_function_scorecard.py` now builds the guarded
  Cloud Function task command and fails closed while auth, entitlement, GPU
  quota, and a real NGC registry container image are absent.
  `templates/ngc/qwen3-v4-peft-scorecard.Containerfile` prepares the benchmark
  container recipe, but no NGC registry image has been built, pushed, or
  selected yet.
- Gaps: no NGC auth, no org/team, no GPU quota, no benchmark container, and no
  result persistence proof.
- Decision: keep NGC blocked until credentials and entitlements are available.
