# Qwen3 V4 PEFT Kaggle P100 Rerun Status

Status: `KernelWorkerStatus.COMPLETE`

Kernel: `edithatogo/qwen3-v4-peft-lm-eval-selected-full`

Artifact directory: `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v2`

Downloaded files: `9`

Recovered summary:
`/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v2/qwen3-v4-peft-kaggle-lm-eval-20260613-233405-summary.json`

## Claim Boundary

No benchmark claim: Kaggle kernel version 2 completed, but the recovered summary
is blocked and has no lm-eval result files.

## Failure Summary

The recovered summary has `status=blocked`, `evaluation.returncode=1`,
`result_files=[]`, `use_4bit=true`, and runtime `torch=2.12.0+cu130`.
`lm_eval` failed while importing `Qwen3ForCausalLM` after a
`torchvision::nms` mismatch.

## Evidence

`kaggle kernels status edithatogo/qwen3-v4-peft-lm-eval-selected-full`
reported:

`edithatogo/qwen3-v4-peft-lm-eval-selected-full has status "KernelWorkerStatus.COMPLETE"`
