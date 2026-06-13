# Plan

## Phase 1 - Endpoint Execution

- [x] Task: started `llama-server` with the cached `gemma-4-E2B_q4_0-it.gguf` artifact on
  `127.0.0.1:18082`.
- [x] Task: ran the queued `strict-suffix-copy-exact` repair through
  `scripts/select_prompt_profile_repair_experiment.py`.
- [x] Task: stopped the endpoint after the run.

## Phase 2 - Result Recording

- [x] Task: captured the strict `1/3` result and source output directory.
- [x] Task: recorded the failure as `completed-no-promotion`.
- [x] Task: kept promotion blocked because the successful case was only the invalid-tool
  refusal, not a valid Hermes tool-call case.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.7 / 10`
- Evidence: endpoint execution is recorded with a report and SSD-backed source
  output path.
- Gaps: raw Hermes tool-call cases remain malformed, so the model is not
  promotable.
