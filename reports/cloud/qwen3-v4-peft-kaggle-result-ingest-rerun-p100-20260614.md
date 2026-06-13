# Qwen3 V4 PEFT Kaggle Result Ingest Gate

Status: `fail`
Summary JSON: `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-rerun-20260614/qwen3-v4-peft-kaggle-lm-eval-20260613-233405-summary.json`
Storage root: `/Volumes/PortableSSD`

## Claim Boundary

No benchmark claim until a scored no-limit Kaggle summary and complete lm-eval results pass this validator.

## Expected Complete Tasks

`arc_challenge`, `hellaswag`, `truthfulqa_mc2`, `gsm8k`, `winogrande`

## Checks

| Check | Result | Detail |
|---|---|---|
| `summary_on_storage_root` | `pass` | /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-rerun-20260614/qwen3-v4-peft-kaggle-lm-eval-20260613-233405-summary.json |
| `status_scored` | `fail` | blocked |
| `adapter_repo_expected` | `pass` | edithatogo/qwen3-4b-hermes-lora-peft-converted |
| `base_model_expected` | `pass` | Qwen/Qwen3-4B |
| `configured_tasks_complete` | `pass` | arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande |
| `no_limit_configured` | `pass` | None |
| `evaluation_returncode_zero` | `fail` | 1 |
| `evaluation_not_timed_out` | `pass` | False |
| `command_has_no_limit_flag` | `pass` | /usr/bin/python3 -m lm_eval --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=/kaggle/working/qwen3-v4-peft-adapter,device_map=auto,dtype=float16,trust_remote_code=True,load_in_4bit=True,bnb_4bit_compute_dtype=float16 --tasks arc_challe |
| `output_dir_on_storage_root` | `fail` | /kaggle/working/qwen3-v4-peft-kaggle-lm-eval-20260613-233405-lm-eval-output |
| `lm_eval_result_present` | `fail` | None |
| `lm_eval_tasks_complete` | `fail` | none |
