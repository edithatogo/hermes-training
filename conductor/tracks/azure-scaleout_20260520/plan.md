# Plan: Azure Scale-Out Preflight and Benchmark Lane

## Phase 1 — Preflight

- [x] Add non-mutating Azure preflight script.
- [x] Log Azure CLI into `d.a.mordaunt@gmail.com`.
- [x] Set default subscription to `Azure for Students`.
- [x] Verify Azure ML CLI extension or install it.
- [x] Run read-only regional quota inspection.

## Phase 2 — Cloud Job Skeleton

- [x] Add Azure ML benchmark job template with Spot/low-priority, scale-to-zero compute assumptions.
- [x] Add Azure ML teacher/evaluator job template for Hermes 4/Qwen3.6/Gemma.
- [x] Add cloud run-card template.
- [x] Add fail-closed benchmark and teacher/evaluator entrypoint skeletons.
- [x] Add Azure ML workspace and low-priority compute YAML templates.
- [x] Add read-only Azure status report script.
- [x] Add Azure GPU quota request notes.

## Phase 3 — First Cloud Proof

- [ ] Run benchmark-only smoke job after preflight passes.
- [ ] Sync report artifacts to SSD.
- [ ] Record costs, VM SKU, region, model revision, and benchmark command.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.4 / 10
- Evidence: preflight script, status script, contracts, docs, Azure ML CLI extension verification, Azure quota-inspection option, workspace/compute/job/run-card skeleton templates, fail-closed job entrypoints, quota request notes, and student account preflight pass for `d.a.mordaunt@gmail.com` / `Azure for Students`.
- Gaps: Azure ML workspace/compute are not created, useful modern GPU quota is zero in `australiaeast`, and first benchmark smoke job remains.
- Decision: account/provider preflight is complete enough for planning; compute creation remains blocked until Azure ML GPU quota/capacity is increased or another region/subscription with quota is selected.
