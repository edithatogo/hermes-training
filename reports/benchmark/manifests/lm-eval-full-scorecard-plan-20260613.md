# lm-evaluation-harness Full Scorecard Plan

Date: 2026-06-13

## Purpose

Run the next Qwen3 v4 selected-task scorecard through the direct MLX lm-eval adapter without a sample limit. This is the first tier that can retire the `lm-eval-selected` missing status in the standard coverage report.

## Plan

- Plan manifest: `reports/benchmark/manifests/lm-eval-full-scorecard-plan-20260613.yaml`
- Run ID: `qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613`
- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613`
- Report: `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613.md`
- Tasks: `arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande`
- Limit: full selected-task run, no `--limit`

## Guardrails

This plan does not launch the benchmark by itself. The full run is expected to be long, resumable, and SSD-backed. Public benchmark claims remain blocked until `summary.json` is scored, every selected task is present in `results.json`, and the standard coverage report is regenerated with `lm-eval-selected` no longer missing.

## Command

```bash
source scripts/env.sh
RUN_ID=qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/$RUN_ID
mkdir -p "$OUT"
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python scripts/run_mlx_lm_eval.py \
  --run-id qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613 \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --tasks arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande \
  --batch-size 1 \
  --max-length 4096 \
  --output-dir "$OUT"
```
