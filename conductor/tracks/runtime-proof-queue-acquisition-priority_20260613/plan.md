# Plan: Runtime Proof Queue Acquisition Priority

## Phase 1 - Priority Model

- [x] Task: Add acquisition-size ordering.
  - [x] Parse total parameter footprint from candidate parameter strings.
  - [x] Keep active/effective size buckets for the existing `size_bucket` field.
  - [x] Sort lane peers by acquisition/storage risk before active-size efficiency.

## Phase 2 - Tests And Queue Output

- [x] Task: Add focused priority coverage.
  - [x] Verify `4B` local proof candidates sort before `80B total / 3B active` candidates.
- [x] Task: Regenerate queue artifacts.
  - [x] Update JSON coverage output.
  - [x] Update Markdown immediate queue.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: The immediate local queue now starts with smaller practical local candidates such as Gemma 4 E4B and Nemotron 3 Nano 4B before 80B-total MoE packages.
- Validation: Focused queue tests, runtime proof queue validation, Conductor consistency, and hub readiness validation are required before commit.
- Gaps: This is queue-prioritization only; it does not establish new benchmark or runtime proof evidence.
- Decision: Complete. The track improves execution order while preserving fail-closed promotion policy.
