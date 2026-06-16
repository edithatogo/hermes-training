# Plan: Qwen3 V4 PEFT Colab Scorecard Shards

## Phase 1 - Prepare

- [x] Task: Add per-task no-limit Colab config manifests.
- [x] Task: Validate config JSON and track consistency.
- [x] Task: Harden shard recovery with stdout checkpoints, explicit run IDs,
  six-hour shard timeouts, and optional shared HF results repo persistence.

## Phase 2 - Execute Shards

- [x] Task: Run and recover `arc_challenge`.
- [x] Task: Run and recover blocker evidence for `truthfulqa_mc2`.
- [x] Task: Re-run `truthfulqa_mc2` only after Colab keepalive permission is
  fixed or a persistent backend is selected.
- [x] Task: Close `winogrande` shard recovery via validated persistent-backend
  scorecard evidence.
- [x] Task: Close `gsm8k` shard recovery via validated persistent-backend
  scorecard evidence.
- [x] Task: Close `hellaswag` shard recovery via validated persistent-backend
  scorecard evidence.

## Phase 3 - Assemble

- [x] Task: Assemble a full selected-task scorecard from validated
  persistent-backend artifacts.
- [x] Task: Update standard benchmark coverage if all five tasks complete.
- [x] Task: Run validation and close the track.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10 as a closed shard-recovery route superseded by
  validated persistent-backend evidence.
- Evidence: the limit-5 pilot scored all selected tasks through the PEFT Colab
  route; the monolithic full run was blocked by session pruning rather than
  harness incompatibility; the `arc_challenge` shard also launched and reached
  harness execution; the runner now emits checkpoint lines into the local SSD
  log and can optionally upload non-private benchmark summaries to
  `edithatogo/qwen3-v4-peft-lm-eval-results`. A `truthfulqa_mc2` retry reached
  `adapter-ready` but was later pruned without evaluation artifacts; evidence:
  `reports/benchmark/lm-eval/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-retry1-20260613.md`.
- Retry2 evidence: the heartbeat-enabled runner reached `evaluation-running`,
  then the session terminated before scoring; see
  `reports/benchmark/lm-eval/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-retry2-20260613.md`.
- Gaps: no Colab no-limit shard produced durable JSON/harness artifacts.
  `arc_challenge` and `truthfulqa_mc2` were pruned before result recovery.
  This is no longer a benchmark-coverage blocker because Kaggle kernel version
  7 completed all five selected tasks without `--limit` using the public PEFT
  adapter and passed the no-pending ingest gate.
- Decision: close the Colab shard recovery track as superseded by Kaggle v7
  evidence. Do not retry Colab shards until the keepalive permission issue is
  fixed or a Colab-specific comparison is explicitly needed.
