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
  ladder, and the bounded adaptive smoke ran live on 2026-06-14. The T4
  attempt lost connection during setup, L4/A100 were rejected for account
  quota/entitlement, and TPU `v5e1` completed the XLA training smoke. Report:
  `reports/colab/colab-gpu-tpu-adaptive-smoke-20260614.md`.
- Gaps: this proves only adaptive smoke execution. PEFT lm-eval scorecards
  remain GPU/persistent-backend workloads and must not be routed to TPU.
