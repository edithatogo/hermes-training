# Qwen3 V4 PEFT Kaggle Scorecard Track

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Metadata: [metadata.json](./metadata.json)
- Requirements: [../../requirements.md](../../requirements.md)
- Design: [../../design.md](../../design.md)
- Contracts: [../../contracts.md](../../contracts.md)

Status: blocked. Kaggle kernel version 1 completed without scoring because
Kaggle assigned a Tesla P100 and the current PyTorch CUDA build does not
support `sm_60`. A fail-closed rerun path is staged with
`torch_compatibility_policy=p100-cu118` and `use_4bit=false`. Kernel version 2
completed and artifacts were recovered to the SSD, but the summary is blocked
with no lm-eval results. The staged runner has been hardened and kernel version
3 has also completed without scores. The staged runner now pins `numpy<2`;
the fixed contract passes. Kernel version 4 completed and artifacts were
recovered to the SSD, but the no-pending ingest gate failed because
`transformers==5.3.0` disabled PyTorch under `torch=2.2.2+cu118`. The staged
runner then pinned `transformers==4.57.6` plus `tokenizers==0.22.2`; kernel
version 5 completed, but the no-pending ingest gate failed because Kaggle still
could not resolve `Qwen3ForCausalLM`. No benchmark claim is allowed; the next
move is a different backend or a different model-loading strategy.
