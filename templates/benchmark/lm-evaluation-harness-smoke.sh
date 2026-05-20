#!/usr/bin/env bash
set -euo pipefail

# Template: lm-evaluation-harness smoke run
# Fill in MODEL_ID and optionally MODEL_REVISION, TASKS, LIMIT, DEVICE, and OUTPUT_PATH.

source scripts/env.sh

MODEL_ID="${MODEL_ID:?set MODEL_ID}"
MODEL_ARGS="pretrained=${MODEL_ID},dtype=float16"

if [[ -n "${MODEL_REVISION:-}" ]]; then
  MODEL_ARGS="${MODEL_ARGS},revision=${MODEL_REVISION}"
fi

TASKS="${TASKS:-arc_challenge,hellaswag,truthfulqa_mc2,gsm8k}"
DEVICE="${DEVICE:-mps}"
BATCH_SIZE="${BATCH_SIZE:-1}"
LIMIT="${LIMIT:-10}"
RUN_ID="${RUN_ID:-$(date +%Y%m%d-%H%M%S)}"
OUTPUT_PATH="${OUTPUT_PATH:-$HERMES_EVAL_ROOT/lm-eval/$RUN_ID}"

lm-eval run \
  --model hf \
  --model_args "${MODEL_ARGS}" \
  --tasks "${TASKS}" \
  --device "${DEVICE}" \
  --batch_size "${BATCH_SIZE}" \
  --limit "${LIMIT}" \
  --output_path "${OUTPUT_PATH}" \
  --log_samples
