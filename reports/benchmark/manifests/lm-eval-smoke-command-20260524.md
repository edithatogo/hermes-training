# lm-evaluation-harness Smoke Command Manifest

Date: 2026-05-24

## Purpose

Run a cheap engineering smoke before broader lm-eval execution.

## Command

```bash
source scripts/env.sh
RUN_ID=qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit10-<date>
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/${RUN_ID}
mkdir -p "$OUT"

/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python scripts/run_mlx_lm_eval.py \
  --run-id "$RUN_ID" \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --tasks arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande \
  --limit 10 \
  --batch-size 1 \
  --max-length 4096 \
  --output-dir "$OUT"
```

## Artifact Root

```text
$HERMES_EVAL_ROOT/lm-eval/<run-id>
```

## Boundary

Limited-sample results are engineering smoke only. Do not publish them as benchmark scores.

Current Qwen3 v4 status: blocked with `mlx_lm.server`. The selected tasks
require loglikelihood scoring; the chat-completions harness is generation-only
for these purposes, and the completions route needs a logprobs-compatible shim.
See
`reports/benchmark/lm-eval/qwen3-4b-v4-targeted-lm-eval-selected-smoke-20260526.md`.

Direct MLX follow-up status: the repo-local `scripts/run_mlx_lm_eval.py`
adapter scored the selected task set at `--limit 10` on 2026-05-26. Treat that
as a bounded smoke only, not a full candidate scorecard. See
`reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit10-20260526.md`.
