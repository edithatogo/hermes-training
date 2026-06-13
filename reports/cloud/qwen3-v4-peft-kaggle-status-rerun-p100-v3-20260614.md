# Qwen3 V4 PEFT Kaggle P100 Rerun V3 Status

Status: `KernelWorkerStatus.COMPLETE`

Kernel: `edithatogo/qwen3-v4-peft-lm-eval-selected-full`

Artifact directory: `/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v3`

Downloaded files: `9`

Recovered summary:
`/Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v3/qwen3-v4-peft-kaggle-lm-eval-20260613-234300-summary.json`

## Claim Boundary

No benchmark claim: Kaggle kernel version 3 completed, but the recovered summary
is blocked and has no lm-eval result files.

## Failure Summary

The recovered summary has `status=blocked`, `evaluation.returncode=1`,
`result_files=[]`, `use_4bit=false`, and runtime `torch=2.2.2+cu118`.
`lm_eval` failed after Torch warned about NumPy 2 incompatibility and
`transformers` could not resolve `Qwen3ForCausalLM`.

## Evidence

`kaggle kernels status edithatogo/qwen3-v4-peft-lm-eval-selected-full`
reported:

`edithatogo/qwen3-v4-peft-lm-eval-selected-full has status "KernelWorkerStatus.COMPLETE"`
