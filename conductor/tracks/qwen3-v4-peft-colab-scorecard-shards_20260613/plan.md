# Plan: Qwen3 V4 PEFT Colab Scorecard Shards

## Phase 1 - Prepare

- [x] Task: Add per-task no-limit Colab config manifests.
- [ ] Task: Validate config JSON and track consistency.

## Phase 2 - Execute Shards

- [ ] Task: Run and recover `arc_challenge`.
- [ ] Task: Run and recover `truthfulqa_mc2`.
- [ ] Task: Run and recover `winogrande`.
- [ ] Task: Run and recover `gsm8k`.
- [ ] Task: Run and recover `hellaswag`.

## Phase 3 - Assemble

- [ ] Task: Assemble a full selected-task scorecard from shard artifacts.
- [ ] Task: Update standard benchmark coverage if all five tasks complete.
- [ ] Task: Run validation and close the track.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 8.7 / 10 while shard execution is pending.
- Evidence: the limit-5 pilot scored all selected tasks through the PEFT Colab
  route; the monolithic full run was blocked by session pruning rather than
  harness incompatibility.
- Gaps: no no-limit shard has been recovered yet.
- Decision: run shorter task-scoped Colab sessions and download artifacts after
  each task.
