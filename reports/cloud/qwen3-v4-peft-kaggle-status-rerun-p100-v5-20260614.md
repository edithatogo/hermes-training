# Qwen3 V4 PEFT Kaggle P100 Rerun V5 Status

Status: `KernelWorkerStatus.COMPLETE`

Kernel: `edithatogo/qwen3-v4-peft-lm-eval-selected-full`

Kernel version: `5`

Artifact directory: `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v5-20260614`

Downloaded files: `15`

Recovered summary:
`/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v5-20260614/qwen3-v4-peft-kaggle-lm-eval-20260614-000150-summary.json`

## Claim Boundary

No benchmark claim: Kaggle kernel version 5 completed, but the recovered summary
is blocked and has no lm-eval result files.

## Failure Summary

The recovered summary has `status=blocked`, `evaluation.returncode=1`,
`result_files=[]`, `use_4bit=false`, runtime `torch=2.2.2+cu118`, and Tesla
P100 capability `6.0`. The runtime pin fixed the PyTorch-disabled failure, but
`transformers==4.57.6` still could not resolve `Qwen3ForCausalLM` in the Kaggle
runtime.

## Evidence

`kaggle kernels status edithatogo/qwen3-v4-peft-lm-eval-selected-full`
reported:

`edithatogo/qwen3-v4-peft-lm-eval-selected-full has status "KernelWorkerStatus.COMPLETE"`
