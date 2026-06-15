# Qwen3 V4 PEFT Kaggle Result Ingest Gate

Status: `pass`
Summary JSON: `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v7-20260614/qwen3-v4-peft-kaggle-lm-eval-20260614-001433-summary.json`
Storage root: `/Volumes/PortableSSD`

## Claim Boundary

No benchmark claim until a scored no-limit Kaggle summary and complete lm-eval results pass this validator.

## Expected Complete Tasks

`arc_challenge`, `hellaswag`, `truthfulqa_mc2`, `gsm8k`, `winogrande`

## Checks

| Check | Result | Detail |
|---|---|---|
| `summary_on_storage_root` | `pass` | /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v7-20260614/qwen3-v4-peft-kaggle-lm-eval-20260614-001433-summary.json |
| `status_scored` | `pass` | scored |
| `adapter_repo_expected` | `pass` | edithatogo/qwen3-4b-hermes-lora-peft-converted |
| `base_model_expected` | `pass` | Qwen/Qwen3-4B |
| `configured_tasks_complete` | `pass` | arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande |
| `no_limit_configured` | `pass` | None |
| `evaluation_returncode_zero` | `pass` | 0 |
| `evaluation_not_timed_out` | `pass` | False |
| `command_has_no_limit_flag` | `pass` | /usr/bin/python3 -m lm_eval --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=/kaggle/working/qwen3-v4-peft-adapter,device_map=auto,dtype=float16,trust_remote_code=True --tasks arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande --b |
| `output_dir_on_storage_root` | `pass` | /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v7-20260614/qwen3-v4-peft-kaggle-lm-eval-20260614-001433-lm-eval-output |
| `lm_eval_result_present` | `pass` | /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v7-20260614/qwen3-v4-peft-kaggle-lm-eval-20260614-001433-lm-eval-output/__kaggle__working__qwen3-v4-peft-adapter/results_2026-06-14T05-41-12.192345.json |
| `lm_eval_tasks_complete` | `pass` | arc_challenge,gsm8k,hellaswag,truthfulqa_mc2,winogrande |
