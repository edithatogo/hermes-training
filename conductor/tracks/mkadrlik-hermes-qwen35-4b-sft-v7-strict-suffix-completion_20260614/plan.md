# Plan: mkadrlik Hermes Qwen3.5 4B SFT v7 Strict-Suffix Completion

## Phase 1: Endpoint Execution

- [x] Task: started `llama-server` with the cached
  `hermes-qwen3.5-4b-Q8_0.gguf` artifact on `127.0.0.1:18086`.
- [x] Task: ran the queued `strict-suffix-copy-exact` repair through
  `scripts/select_prompt_profile_repair_experiment.py`.
- [x] Task: stopped the endpoint after the run.

## Phase 2: Result Recording

- [x] Task: captured the strict `1/3` result and source output directory.
- [x] Task: recorded the failure as `completed-no-promotion`.
- [x] Task: kept promotion blocked because parallel envelopes and refusal
  wording failed.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: endpoint execution is recorded with a report and SSD-backed source
  output path.
- Gaps: parallel-call output is malformed and unavailable-tool refusal leaks the
  forbidden tool name.
