# Plan

## Phase 1 - Endpoint Execution

- [x] Task: started `llama-server` with the cached `EXAONE-4.0-1.2B-Q4_K_M.gguf`
  artifact on `127.0.0.1:18081`.
- [x] Task: ran the queued `strict-suffix-copy-exact` repair through
  `scripts/select_prompt_profile_repair_experiment.py`.
- [x] Task: stopped the endpoint after the run.

## Phase 2 - Result Recording

- [x] Task: captured the strict `0/3` result and source output directory.
- [x] Task: recorded the failure as `completed-no-promotion`.
- [x] Task: kept promotion blocked pending a different model, constrained decoding, or a
  downstream envelope/grammar route.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: endpoint execution is recorded with a report and SSD-backed source
  output path.
- Gaps: the model is not promotable and needs a separate constrained-output
  track if revisited.
