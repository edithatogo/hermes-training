# Qwen3 V4 PEFT HF Jobs Scorecard Plan

Status: `prepared-not-submitted`

## Rationale

Colab T4 scored the bounded route pilot but pruned no-limit runs before result
artifacts could be recovered. HF Jobs is authenticated locally as `edithatogo`
and exposes persistent GPU job hardware, so it is the next viable backend for
the no-limit selected-task scorecard.

## Prepared Artifact

Public PEFT adapter repo:

```text
edithatogo/qwen3-4b-hermes-lora-peft-converted
```

Job config:

```text
reports/benchmark/manifests/qwen3-v4-peft-hf-jobs-lm-eval-selected-full-config-20260613.json
```

The config expects the adapter repo mounted read-only at `/adapter`.

Results repo:

```text
https://huggingface.co/datasets/edithatogo/qwen3-v4-peft-lm-eval-results
```

## Candidate Command

This command is intentionally not executed in this commit because HF Jobs GPU
hardware is paid. It should be run after explicit paid-compute approval:

```bash
hf jobs run \
  --flavor t4-small \
  --timeout 8h \
  --detach \
  --secrets HF_TOKEN \
  -e RUN_ID=qwen3-v4-peft-hf-jobs-lm-eval-selected-full-20260613 \
  -e HF_RESULTS_REPO=edithatogo/qwen3-v4-peft-lm-eval-results \
  -e LM_EVAL_TASKS=arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande \
  -e LM_EVAL_TIMEOUT_S=21600 \
  -v hf://models/edithatogo/qwen3-4b-hermes-lora-peft-converted:/adapter:ro \
  pytorch/pytorch:2.7.1-cuda12.6-cudnn9-runtime \
  bash -lc 'python -m pip install --quiet --upgrade "lm_eval[hf]" "transformers>=4.56,<5" peft bitsandbytes safetensors accelerate huggingface_hub && curl -L https://raw.githubusercontent.com/edithatogo/hermes-training/main/scripts/hf_jobs_peft_lm_eval_selected.py -o /tmp/hf_jobs_peft_lm_eval_selected.py && python /tmp/hf_jobs_peft_lm_eval_selected.py'
```

The job payload uploads `/tmp/<run-id>/summary.json` and any
`lm-eval` output files to `edithatogo/qwen3-v4-peft-lm-eval-results` when
`HF_TOKEN` is passed as a secret.

## Hardware Options Observed

`hf jobs hardware` listed:

- `t4-small`: 1x T4, $0.40/hour
- `t4-medium`: 1x T4, $0.60/hour
- `l4x1`: 1x L4, $0.80/hour
- `a10g-small`: 1x A10G, $1.00/hour
- `a100-large`: 1x A100, $2.50/hour

## Stop Conditions

- No paid GPU job without explicit approval.
- No public no-limit benchmark claim until all five selected tasks complete
  without `--limit`.
- If HF Jobs cannot persist artifacts to a Hub dataset/bucket, use Azure or NGC
  instead.
