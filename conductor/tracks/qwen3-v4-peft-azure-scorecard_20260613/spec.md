# Specification: Qwen3 V4 PEFT Azure Scorecard

## Overview

Prepare Azure ML as the next persistent backend for the Qwen3 v4 PEFT
no-limit selected-task `lm_eval[hf]` scorecard, after Colab pruning and HF Jobs
credit blockers.

## Acceptance Criteria

- Add a guarded Azure ML submitter that dry-runs by default.
- Add a Qwen3 v4 PEFT Azure ML command-job template.
- Record the current Azure login blocker without creating resources.
- Refuse live submission unless Azure login, ML extension, job template, and
  explicit confirmation are present.
- Do not claim full benchmark coverage until Azure completes all selected tasks
  without `--limit` and artifacts are downloaded to `/Volumes/PortableSSD`.

## Out Of Scope

- Running `az login` on behalf of the user.
- Creating resource groups, workspaces, compute, environments, or jobs before
  account/quota/cost gates pass.
- Uploading private datasets or secrets.
