# Plan: Gemma 4 No-Thinking Dataset Guard

## Phase 1: Scripts

- [x] Task: add `scripts/materialize_gemma4_no_thinking_dataset.py`.
- [x] Task: add `scripts/validate_gemma4_no_thinking_dataset.py`.
- [x] Task: add unit tests for materialization and validation.

## Phase 2: Data And Configs

- [x] Task: materialize Gemma-specific no-thinking copies of the shared splits.
- [x] Task: materialize Gemma-specific no-thinking copies of the v6 free-text-copy
  strict tool-call splits.
- [x] Task: retarget the Gemma 4 26B A4B experimental configs and set the
  explicit enforcement flag.

## Phase 3: Conductor And Validation

- [x] Task: add nested `gemma4` Conductor track and contract update.
- [x] Task: add hub Conductor track and dataset evidence note.
- [x] Task: run focused tests, Conductor consistency, and full readiness.
- [x] Task: commit and push the nested `gemma4` repo before the hub pointer.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: unit tests, Gemma 4 validator, Conductor consistency, and full
  readiness passed.
- Gaps: this is prerequisite formatting work; training and broad benchmarks
  remain separate gated tracks.
