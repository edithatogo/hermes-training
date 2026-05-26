# lm-evaluation-harness Candidate Command Manifest

Date: 2026-05-24

## Purpose

Run a broader local comparability pass after a model clears runtime smoke and the local strict tool-call gate.

## Gate

- Candidate must have a stable endpoint or local adapter supported by `lm-evaluation-harness`.
- Candidate must have SSD-backed raw output roots.
- Candidate must have a run card with model revision, adapter revision, runtime version, prompt template, and sampling settings.

## Command

```bash
source scripts/env.sh
RUN_ID=<model>-lm-eval-candidate-<date>
MODEL_ID=<runtime_model_id>
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/${RUN_ID}
mkdir -p "$OUT"

/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python scripts/run_mlx_lm_eval.py \
  --run-id "$RUN_ID" \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --tasks arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande \
  --batch-size 1 \
  --max-length 4096 \
  --output-dir "$OUT"
```

Use the smoke manifest first with `--limit 10`. This candidate command is the
next tier and should not be used for external claims until the full selected
task run completes, raw `results.json` is retained, and reviewer sign-off is
recorded.

Current Qwen3 v4 status: endpoint-based `lm_eval` remains blocked with
`mlx_lm.server` because the selected tasks require prompt loglikelihood and the
server does not return legacy echoed `token_logprobs`. The direct MLX adapter
has scored a `--limit 10` selected-task smoke, but the full candidate run is
still missing. See
`reports/benchmark/lm-eval/qwen3-4b-v4-targeted-lm-eval-selected-smoke-20260526.md`
and
`reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit10-20260526.md`.

## Result Card Schema

```json
{
  "run_id": "<model>-lm-eval-candidate-<date>",
  "suite": "lm-eval-candidate",
  "model": "<runtime_model_id>",
  "tasks": ["arc_challenge", "hellaswag", "truthfulqa_mc2", "gsm8k", "winogrande"],
  "raw_output": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/<run-id>",
  "report": "reports/benchmark/lm-eval/<run-id>.md",
  "harness_version": null,
  "normalized_scores": {},
  "known_failures": [],
  "publish_decision": "internal-candidate"
}
```

## Publication Boundary

Candidate results can inform model selection, but public claims require full harness metadata, deterministic rerun notes, and reviewer sign-off.
