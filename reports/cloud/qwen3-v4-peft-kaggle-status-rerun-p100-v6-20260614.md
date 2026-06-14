# Qwen3 V4 PEFT Kaggle P100 Rerun V6 Status

Status: `KernelWorkerStatus.COMPLETE`

Kernel: `edithatogo/qwen3-v4-peft-lm-eval-selected-full`

Kernel version: `6`

Artifact directory: `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v6-20260614`

Downloaded files: `2`

Recovered summary:
`/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v6-20260614/qwen3-v4-peft-kaggle-lm-eval-20260614-000917-summary.json`

## Claim Boundary

No benchmark claim: Kaggle kernel version 6 completed, but the recovered summary
is blocked before lm-eval scoring.

## Failure Summary

The recovered summary has `status=blocked`. The direct Qwen3 import probe failed
before lm-eval because Kaggle's preinstalled `torchao` imported `quantizer_torchao` and expected
`torch._C.Tag.needs_fixed_stride_order`, which is absent from
`torch==2.2.2+cu118`. The staged runner now removes `torchao` on the non-4-bit
P100 path before applying the P100 torch policy.

## Evidence

`kaggle kernels status edithatogo/qwen3-v4-peft-lm-eval-selected-full`
reported:

`edithatogo/qwen3-v4-peft-lm-eval-selected-full has status "KernelWorkerStatus.COMPLETE"`
