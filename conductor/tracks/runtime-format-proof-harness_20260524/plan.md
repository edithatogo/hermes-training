# Plan: Runtime Format Proof Harness

## Phase 1 - Proof Card Template

- [x] Task: Add a lane proof-card template with identity, lane contract, command, checklist, results, and notes.

## Phase 2 - Generator

- [x] Task: Add `scripts/create_runtime_format_lane_card.py`.
- [x] Task: Default generated cards to `/Volumes/PortableSSD/hermes-evals/runtime-format-lanes/`.
- [x] Task: Support `--print` preview mode.

## Phase 3 - Validation And Manifest

- [x] Task: Add tests for lane validation and rendered proof-card content.
- [x] Task: Add a runtime format lane proof manifest.
- [x] Task: Wire the generator into readiness syntax checks.
- [x] Task: Run validation.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: `templates/runtime/format-lane-proof-card.md`, `scripts/create_runtime_format_lane_card.py`, `tests/test_runtime_format_lanes.py`, and `reports/runtime/runtime-format-lane-proof-manifest-20260524.md` operationalize the format ladder without downloading models.
- Remaining gaps: Each lane still needs real runtime or training proof before promotion.
