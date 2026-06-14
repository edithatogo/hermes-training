# Qwen3 V4 PEFT Kaggle Scorecard Track

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Metadata: [metadata.json](./metadata.json)
- Requirements: [../../requirements.md](../../requirements.md)
- Design: [../../design.md](../../design.md)
- Contracts: [../../contracts.md](../../contracts.md)

Status: blocked pending external run completion. Kaggle kernel versions 1-6 all
completed without scores and each failure is captured by the fail-closed result
ingest reports. The current staged P100 runner now disables 4-bit, pins
`numpy<2`, uses `transformers==4.57.6` plus `tokenizers==0.22.2`, disables
TensorFlow/Flax discovery, applies `torch==2.2.2+cu118` last, and removes
Kaggle's incompatible preinstalled `torchao` package before the Qwen3 import
probe. Kernel version 7 was submitted from that runner and remains
`KernelWorkerStatus.RUNNING`; no artifacts from that run have been recovered
yet. No benchmark claim is allowed until v7 completes, SSD artifacts are
downloaded, and the no-pending ingest gate passes.
