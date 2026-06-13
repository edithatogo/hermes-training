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

- [x] Task: Attempt a minimal persistent HF Jobs route submission.
- [x] Task: Record the live HF Jobs credit blocker.
- [ ] Task: Submit the job and capture job ID/log URL after credits/grant are available.
- [ ] Task: Download result artifacts and update benchmark coverage if complete.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.5 / 10 as a prepared-but-blocked backend track.
- Evidence: HF CLI is authenticated as `edithatogo`; HF Jobs hardware is
  available; PEFT adapter is now publicly mounted from the Hub; a Docker job
  payload can upload results to a Hub dataset.
- Gaps: live HF Jobs submission returned `402 Payment Required` because the
  prepaid credit balance is insufficient; no job ID was created and artifact
  persistence has not yet been live-tested.
- Decision: keep HF Jobs prepared but blocked until credits or a grant are
  available; use Azure after login/quota preflight as the next persistent
  backend candidate.
