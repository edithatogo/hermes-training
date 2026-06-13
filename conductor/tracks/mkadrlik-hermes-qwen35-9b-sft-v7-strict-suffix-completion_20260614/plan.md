# Plan: mkadrlik Hermes Qwen3.5 9B SFT v7 Strict-Suffix Completion

## Phase 1: Endpoint Execution

- [x] Task: started `llama-server` with the cached
  `hermes-qwen3.5-9b-Q4_K_M.gguf` artifact on `127.0.0.1:18087`.
- [x] Task: ran the queued `strict-suffix-copy-exact` repair through
  `scripts/select_prompt_profile_repair_experiment.py`.
- [x] Task: stopped the endpoint after the run.

## Phase 2: Result Recording

- [x] Task: captured the strict `1/3` result and source output directory.
- [x] Task: recorded the failure as `completed-no-promotion`.
- [x] Task: kept promotion blocked because available-tool calls failed strict
  Hermes parsing.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: endpoint execution is recorded with a report and SSD-backed source
  output path.
- Gaps: tool payloads use `parameters` and parallel envelopes are malformed.
