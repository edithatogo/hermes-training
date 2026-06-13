# Plan: ManiacLabs Qwen3.6 35B A3B 2bit Empty-Output Retry Completion

## Phase 1: Endpoint Execution

- [x] Task: started `llama-server` with the cached
  `qwen3.6-35b-a3b-iq2xxs-q2k.gguf` artifact on `127.0.0.1:18084`.
- [x] Task: ran the queued `empty-output-retry` repair through
  `scripts/select_prompt_profile_repair_experiment.py`.
- [x] Task: stopped the endpoint after the run.

## Phase 2: Result Recording

- [x] Task: captured the strict `2/3` result and source output directory.
- [x] Task: recorded the failure as `completed-no-promotion`.
- [x] Task: kept promotion blocked because the single lookup case still
  produced a malformed Hermes envelope.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: endpoint execution is recorded with a report and SSD-backed source
  output path.
- Gaps: one raw Hermes tool-call envelope remains malformed.
