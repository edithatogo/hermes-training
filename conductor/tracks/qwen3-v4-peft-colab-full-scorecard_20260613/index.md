# Qwen3 V4 PEFT Colab Full Scorecard Track

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Metadata: [metadata.json](./metadata.json)
- Requirements: [../../requirements.md](../../requirements.md)
- Design: [../../design.md](../../design.md)
- Contracts: [../../contracts.md](../../contracts.md)

Status: complete. The Colab T4 no-limit run reached harness execution but its
JSON and harness artifacts were not recoverable after the session was pruned by
the known keepalive permission blocker. The track is closed as superseded
because Kaggle kernel version 7 completed the same no-limit selected-task PEFT
scorecard, recovered artifacts to `/Volumes/PortableSSD`, and passed the
no-pending ingest gate in
`reports/cloud/qwen3-v4-peft-kaggle-result-ingest-rerun-p100-v7-20260614.md`.
Do not retry Colab no-limit scoring unless the keepalive permission issue is
fixed or a Colab-specific comparison is explicitly required.
