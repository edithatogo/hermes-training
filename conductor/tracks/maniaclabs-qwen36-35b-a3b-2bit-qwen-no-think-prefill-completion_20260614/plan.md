# Plan: ManiacLabs Qwen3.6 35B A3B 2bit Qwen No-Think Prefill Completion

## Phase 1: Endpoint Execution

- [x] Task: started `llama-server` with the cached
  `qwen3.6-35b-a3b-iq2xxs-q2k.gguf` artifact on `127.0.0.1:18084`.
- [x] Task: ran the queued `qwen-no-think-prefill` repair through
  `scripts/select_prompt_profile_repair_experiment.py`.
- [x] Task: stopped the endpoint after the run.

## Phase 2: Result Recording

- [x] Task: captured the strict `1/3` result and source output directory.
- [x] Task: recorded the failure as `completed-no-promotion`.
- [x] Task: kept promotion blocked because visible `<think>` text and
  non-Hermes tool structures failed strict raw-output scoring.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: endpoint execution is recorded with a report and SSD-backed source
  output path.
- Gaps: no-think/prefill is harmful for this endpoint profile.
