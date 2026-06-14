# Qwen3 V4 PEFT Kaggle P100 Rerun V4 Status

Status: `KernelWorkerStatus.COMPLETE`

Kernel: `edithatogo/qwen3-v4-peft-lm-eval-selected-full`

Kernel version: `4`

Artifact directory: `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v4-20260614`

Downloaded files: `16`

Recovered summary:
`/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v4-20260614/qwen3-v4-peft-kaggle-lm-eval-20260613-235158-summary.json`

## Claim Boundary

No benchmark claim: Kaggle kernel version 4 completed, but the recovered summary
is blocked and has no lm-eval result files.

## Failure Summary

The recovered summary has `status=blocked`, `evaluation.returncode=1`,
`result_files=[]`, `use_4bit=false`, runtime `torch=2.2.2+cu118`, and Tesla
P100 capability `6.0`. `lm_eval` failed because `transformers==5.3.0` disables
PyTorch when `torch<2.4`, so `AutoModelForCausalLM` reported PyTorch
unavailable.

## Evidence

`kaggle kernels status edithatogo/qwen3-v4-peft-lm-eval-selected-full`
reported:

`edithatogo/qwen3-v4-peft-lm-eval-selected-full has status "KernelWorkerStatus.COMPLETE"`
