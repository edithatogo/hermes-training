# Plan: HF Jobs Python Executable Payload

## Phase 1 - Submitter Contract

- [x] Task: Add a configurable payload Python executable.
  - [x] Add the field to `HfJobsScorecardSpec`.
  - [x] Use it for `-m pip` and script execution.
  - [x] Expose `--python-executable` in the CLI.

## Phase 2 - Evidence

- [x] Task: Regenerate the HF Jobs dry-run JSON.
  - [x] Record `python_executable`.
  - [x] Preserve dry-run status and paid-compute gates.

## Phase 3 - Validation

- [x] Task: Add unit coverage for custom interpreter payloads.
- [x] Task: Run HF Jobs submitter tests.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: The submitter can now generate payloads for images that require `python3` or another interpreter while keeping the default unchanged.
- Validation: HF Jobs submitter tests, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: HF Jobs remains blocked by prepaid credits/grant capacity and no remote run was submitted.
- Decision: Complete. The dry-run contract is more portable without weakening paid-compute gates.
