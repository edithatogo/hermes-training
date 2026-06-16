# Qwen3 v4 PEFT Lightning Scorecard Track

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Metadata: [metadata.json](./metadata.json)
- Requirements: [../../requirements.md](../../requirements.md)
- Design: [../../design.md](../../design.md)
- Contracts: [../../contracts.md](../../contracts.md)

Status: complete. Lightning Jobs is prepared as a guarded fallback with a
dry-run submitter, staged config, confirmation gates, and cloud-report commands.
No Lightning login or job submission was run because Teamspace, machine policy,
free credit/grant, and explicit approval were not proven. The route is closed
as prepared/deferred because Kaggle kernel version 7 completed the current
no-limit selected-task scorecard and passed the no-pending ingest gate. Do not
run Lightning login or submit jobs unless the user explicitly chooses Lightning
for cross-provider comparison and confirms account/cost gates.
