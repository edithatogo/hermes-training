# Qwen3 V4 PEFT Kaggle P100 Rerun V5 Status

Status: `KernelWorkerStatus.RUNNING`

Kernel: `edithatogo/qwen3-v4-peft-lm-eval-selected-full`

Kernel version: `5`

Artifact directory: `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v5-20260614`

Downloaded files: `0`

## Claim Boundary

No benchmark claim while Kaggle kernel version 5 is still running. Scores
require SSD artifact recovery plus no-pending ingest validation after
completion.

## Running Summary

Kernel version 5 is running after the staged runner changed to
`transformers==4.57.6` plus `tokenizers==0.22.2`. The next gates are to poll for
completion, recover `/kaggle/working` artifacts to the SSD path above, and run
the no-pending ingest validator before any benchmark claim.

## Evidence

`kaggle kernels status edithatogo/qwen3-v4-peft-lm-eval-selected-full`
reported:

`edithatogo/qwen3-v4-peft-lm-eval-selected-full has status "KernelWorkerStatus.RUNNING"`
