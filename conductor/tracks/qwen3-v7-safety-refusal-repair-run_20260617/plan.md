# Plan: Qwen3 v7 Safety/Refusal Repair Run

## Phase 1 - Training

- [x] Task: dry-run the v7 training config.
- [x] Task: run the bounded 160-iteration MLX LoRA repair job.
- [x] Task: confirm adapter artifacts remain ignored.

## Phase 2 - Rerun And Ingest

- [x] Task: rerun the pinned safety/refusal suite with the v7 adapter.
- [x] Task: store raw benchmark artifacts on `/Volumes/PortableSSD`.
- [x] Task: add the compact repair-run report builder.
- [x] Task: add the compact repair-run report validator.
- [x] Task: add focused unit tests.

## Phase 3 - Readiness And Handoff

- [x] Task: wire the validator into `scripts/validate_readiness.py`.
- [x] Task: generate JSON and Markdown reports.
- [x] Task: add this Conductor track to the registry.
- [x] Task: keep publication blocked because target gates were not met.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: training completed, the safety/refusal rerun completed, raw outputs
  are SSD-backed, compact reports are validator-backed, and full readiness
  includes the new report gate.
- Remaining gap: v7 improved but did not pass. Strict pass rose from 0.125 to
  0.375, invalid-tool handling from 0.200 to 0.600, and empty-think wrappers
  still appear in all 8 responses.
- Decision: complete this result-ingest track. The next implementation should
  target wrapper removal and the remaining security/exfiltration refusal leaks.
