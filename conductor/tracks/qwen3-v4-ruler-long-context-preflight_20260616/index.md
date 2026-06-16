# Qwen3 v4 RULER Long-Context Preflight Track

- Spec: [spec.md](./spec.md)
- Plan: [plan.md](./plan.md)
- Metadata: [metadata.json](./metadata.json)
- Requirements: [../../requirements.md](../../requirements.md)
- Design: [../../design.md](../../design.md)
- Contracts: [../../contracts.md](../../contracts.md)

Status: complete as a launch-gate setup track. The first RULER stage is fixed
at `ctx4096`, with a 4096/8192/16384 context ladder recorded. Execution remains
blocked because the SSD benchmark environment does not currently provide the
`ruler` module.
