# Qwen3 V4 PEFT Kaggle Scorecard Track

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Metadata: [metadata.json](./metadata.json)
- Requirements: [../../requirements.md](../../requirements.md)
- Design: [../../design.md](../../design.md)
- Contracts: [../../contracts.md](../../contracts.md)

Status: complete. Kaggle kernel versions 1-6 all completed without scores and
each failure is captured by the fail-closed result ingest reports. Kernel
version 7 completed on a Tesla P100 with the hardened runner: 4-bit disabled,
`numpy<2`, `transformers==4.57.6`, `tokenizers==0.22.2`, TensorFlow/Flax
discovery disabled, `torch==2.2.2+cu118` applied last, and Kaggle's
incompatible preinstalled `torchao` removed before the Qwen3 import probe. The
SSD-recovered summary and lm-eval results passed the strict no-pending ingest
gate in `reports/cloud/qwen3-v4-peft-kaggle-result-ingest-rerun-p100-v7-20260614.md`.
The no-limit selected-task scorecard is now valid evidence for
`lm-eval-selected` coverage, while BFCL, coding, safety, and RULER official
candidate suites remain separate missing benchmarks.
