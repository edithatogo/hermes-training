# Implementation Plan

## Phase 1: Fail-Closed Publication Command

- [x] Task: Add HF adapter package publication preflight
    - [x] Validate required adapter package files.
    - [x] Validate package location under the SSD export root.
    - [x] Validate package manifest target repo consistency.
    - [x] Report remaining manifest blockers.
- [x] Task: Add explicit approval gate
    - [x] Print the exact approval phrase.
    - [x] Require `--publish` before any upload action.
    - [x] Require an approval file containing the exact phrase when `--publish`
      is requested.
- [x] Task: Validate fail-closed behavior
    - [x] Run dry-run JSON validation against the v6 package.
    - [x] Run publish-mode validation without approval and confirm it blocks.
    - [x] Run hub readiness validation.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Documentation And Checkpoint

- [x] Task: Record publication-gate evidence
    - [x] Add a v6 publication-gate report with dry-run and blocked-publish
      outputs.
    - [x] Update the track health estimate to `>= 9.5 / 10`.
- [x] Task: Mark track complete
    - [x] Update metadata status.
    - [x] Update `conductor/tracks.md`.
    - [x] Commit and push the scoped changes.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Health Target

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: package dry-run validation, publish-mode failure without approval,
  Python syntax validation, and hub readiness validation.
- Remaining gaps: external HF publication remains intentionally blocked until
  final model-card review, benchmark-scope decision, and explicit human
  approval are recorded.
