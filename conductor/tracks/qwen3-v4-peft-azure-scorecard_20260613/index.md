# Qwen3 V4 PEFT Azure Scorecard Track

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Metadata: [metadata.json](./metadata.json)
- Requirements: [../../requirements.md](../../requirements.md)
- Design: [../../design.md](../../design.md)
- Contracts: [../../contracts.md](../../contracts.md)

Status: complete. Azure ML is prepared as a guarded fallback route, but live
login, quota checks, workspace/compute creation, and job submission remain
account-side operations outside this track's safe execution boundary. The route
is closed as prepared/deferred because Kaggle kernel version 7 completed the
current no-limit selected-task scorecard and passed the no-pending ingest gate.
Do not run `az login`, create Azure resources, or submit jobs unless the user
explicitly chooses Azure for cross-provider comparison and confirms quota/cost
gates.
