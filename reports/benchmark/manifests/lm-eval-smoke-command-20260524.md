# lm-evaluation-harness Smoke Command Manifest

Date: 2026-05-24

## Purpose

Run a cheap engineering smoke before broader lm-eval execution.

## Command

```bash
source scripts/env.sh
MODEL_ID=<model_id_or_path> \
TASKS=arc_challenge,hellaswag,truthfulqa_mc2,gsm8k \
LIMIT=10 \
RUN_ID=<model>-lm-eval-smoke-<date> \
  bash templates/benchmark/lm-evaluation-harness-smoke.sh
```

## Artifact Root

```text
$HERMES_EVAL_ROOT/lm-eval/<run-id>
```

## Boundary

Limited-sample results are engineering smoke only. Do not publish them as benchmark scores.
