# Specification: Qwen3 V4 PEFT Colab Scorecard Shards

## Overview

Execute the no-limit selected-task `lm-eval` scorecard as one Colab T4 session
per task, using the validated converted PEFT adapter route. This is a recovery
strategy for the monolithic full run, which was pruned before producing
artifacts.

## Acceptance Criteria

- Add per-task config manifests for `arc_challenge`, `hellaswag`,
  `truthfulqa_mc2`, `gsm8k`, and `winogrande`.
- For each shard, upload the adapter tarball and the task config to a clean
  Colab T4 session, run `scripts/colab_peft_lm_eval_selected.py`, download the
  JSON and harness result, and terminate the session.
- Record a tracked shard report for each task.
- Assemble a final selected-task scorecard report only after all five shards
  have no-limit result artifacts.

## Out Of Scope

- Changing task definitions or prompt formats.
- Combining bounded pilot results with no-limit shard results.
- Publishing no-limit coverage before all five shards complete.
