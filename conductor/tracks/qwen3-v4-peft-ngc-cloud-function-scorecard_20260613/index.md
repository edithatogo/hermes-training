# Qwen3 V4 PEFT NGC Cloud Function Scorecard Track

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Metadata: [metadata.json](./metadata.json)
- Requirements: [../../requirements.md](../../requirements.md)
- Design: [../../design.md](../../design.md)
- Contracts: [../../contracts.md](../../contracts.md)

Status: complete. NGC discovery and fail-closed gating are complete: the CLI
surface, missing `ngc batch` route, likely Cloud Function task route, auth/org/
team/quota/container blockers, guarded submitter, and container recipe are all
recorded. No NGC auth, image push, or task submission was run. The route is
closed as a guarded discovery fallback because Kaggle kernel version 7 completed
the current no-limit selected-task scorecard and passed the no-pending ingest
gate. Do not configure NGC auth, push containers, or submit tasks unless
credentials/entitlements are provided and NGC is explicitly chosen for
cross-provider comparison.
