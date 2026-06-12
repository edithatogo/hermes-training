# Plan: Tiny Helper Standard Benchmark Execution

## Phase 1: Execution Setup

- [ ] Task: confirm the exact benchmark commands and artifact roots for the
  tiny helper candidates.
- [ ] Task: choose the initial candidate order and lock the comparison lane.
- [ ] Task: verify the local prompt coverage and helper profile baseline.

## Phase 2: Benchmark Execution

- [ ] Task: run the Hermes-local expanded prompt set for the tiny helper
  candidates.
- [ ] Task: run the applicable BFCL-style subset for the lane.
- [ ] Task: run any lightweight IFEval or coding subset that the repo already
  supports for this lane.
- [ ] Task: record blocked subsets explicitly instead of skipping them silently.

## Phase 3: Evidence And Documentation

- [ ] Task: write run cards and benchmark summaries for the executed subsets.
- [ ] Task: update `HANDOFF.md`, `FUTURE_MODELS.md`, and any related radar
  notes with the execution outcome.
- [ ] Task: run validation and whitespace checks.
- [ ] Task: mark the track complete only after the evidence is recorded.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.4 / 10
- Evidence: prompt coverage is already valid at 100 prompts per set, and the
  tiny helper lane has a dedicated runtime profile.
- Gaps: the subset execution and result capture are still pending.
