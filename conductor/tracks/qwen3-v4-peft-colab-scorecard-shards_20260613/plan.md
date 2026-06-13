# Plan: Qwen3 V4 PEFT Colab Scorecard Shards

## Phase 1 - Prepare

- [x] Task: Add per-task no-limit Colab config manifests.
- [x] Task: Validate config JSON and track consistency.

## Phase 2 - Execute Shards

- [x] Task: Run and recover `arc_challenge`.
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
- Current estimate: 7.6 / 10 while blocked on Colab session pruning.
- Evidence: the limit-5 pilot scored all selected tasks through the PEFT Colab
  route; the monolithic full run was blocked by session pruning rather than
  harness incompatibility; the `arc_challenge` shard also launched and reached
  harness execution.
- Gaps: no no-limit shard has been recovered; `arc_challenge` was pruned before
  JSON or harness artifacts were downloadable.
- Decision: pause further Colab no-limit shards until keepalive permissions or
  persistent external artifact storage are fixed.
