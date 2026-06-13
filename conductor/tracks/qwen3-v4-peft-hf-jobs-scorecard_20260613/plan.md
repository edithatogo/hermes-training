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

## Phase 3 - Execute

- [ ] Task: Obtain explicit paid GPU approval or a no-cost HF Jobs grant.
- [ ] Task: Submit the job and capture job ID/log URL.
- [ ] Task: Download result artifacts and update benchmark coverage if complete.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.1 / 10 while execution is approval-gated.
- Evidence: HF CLI is authenticated as `edithatogo`; HF Jobs hardware is
  available; PEFT adapter is now publicly mounted from the Hub; a Docker job
  payload can upload results to a Hub dataset.
- Gaps: no paid HF Jobs GPU run has been submitted; job artifact persistence
  has not yet been live-tested.
- Decision: use HF Jobs as the next persistent backend once paid-compute
  approval and job payload persistence are in place.
