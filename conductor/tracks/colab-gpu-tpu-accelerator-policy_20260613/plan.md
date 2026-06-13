# Plan: Colab GPU/TPU Accelerator Policy

## Phase 1: Policy

- [x] Task: add the Colab GPU/TPU accelerator ladder to cloud preflight.
- [x] Task: mark TPU as opt-in and restrict it to adaptive scripts.
- [x] Task: document TPU-incompatible scorecard workloads.

## Phase 2: Reports

- [x] Task: regenerate backend preflight, unblock checklist, and active blocked
  track matrix.
- [x] Task: update handoff notes with the operational decision.

## Phase 3: Validation

- [x] Task: add unit tests for Colab preflight policy and dispatcher parsing.
- [x] Task: run focused cloud/Colab tests.
- [x] Task: run full readiness.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: cloud reports now expose the policy, tests cover the accelerator
  ladder, and no live remote runtime was created.
- Gaps: actual Colab TPU availability is still a live execution question; this
  track only prepares fail-closed routing.
