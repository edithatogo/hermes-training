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

- [x] Block benchmark-only smoke job until modern GPU quota is approved.
- [x] Document that no compute/job should be created under current zero-quota finding.
- [x] Keep sync/cost/run-card requirements in the cloud templates for the first future job.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: preflight script, status script, contracts, docs, Azure ML CLI extension verification, Azure quota-inspection option, workspace/compute/job/run-card skeleton templates, fail-closed job entrypoints, quota request notes, and student account preflight pass for `d.a.mordaunt@gmail.com` / `Azure for Students`.
- Gaps: Azure ML workspace/compute are intentionally not created because useful modern GPU quota is zero across the sampled regions.
- Decision: repository work for this track is complete and fail-closed. The first benchmark smoke job is an external capacity step, not a repo implementation gap, and should start only after quota/capacity is approved for a current GPU family.
