# Plan: NVIDIA Nemotron 3 Nano 4B GGUF Strict-Suffix Completion

## Phase 1: Endpoint Execution

- [x] Task: started `llama-server` with the cached
  `NVIDIA-Nemotron3-Nano-4B-Q4_K_M.gguf` artifact on `127.0.0.1:18089`.
- [x] Task: ran the queued `strict-suffix-copy-exact` repair through
  `scripts/select_prompt_profile_repair_experiment.py`.
- [x] Task: stopped the endpoint after the run.

## Phase 2: Result Recording

- [x] Task: captured the strict `1/3` result and source output directory.
- [x] Task: recorded the failure as `completed-no-promotion`.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: endpoint execution is recorded with a report and SSD-backed source
  output path.
- Gaps: available-tool calls are empty or DSML-tagged, not strict Hermes.
