# Qwen3 V4 PEFT HF Jobs Scorecard Track

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Metadata: [metadata.json](./metadata.json)
- Requirements: [../../requirements.md](../../requirements.md)
- Design: [../../design.md](../../design.md)
- Contracts: [../../contracts.md](../../contracts.md)

Status: complete. HF Jobs is prepared as a fallback execution route with a
public PEFT adapter and guarded submitter, but live submission returned
`402 Payment Required` because prepaid credits were insufficient. The route is
closed as prepared/deferred because Kaggle kernel version 7 completed the
current no-limit selected-task scorecard and passed the no-pending ingest gate.
Do not submit HF Jobs unless credits/grant capacity becomes available and a
cross-provider comparison is explicitly required.
