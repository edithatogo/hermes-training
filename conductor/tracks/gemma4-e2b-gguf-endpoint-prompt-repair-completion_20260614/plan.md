# Plan

## Phase 1 - Endpoint Execution

Status: completed

- Started `llama-server` with the cached `gemma-4-E2B_q4_0-it.gguf` artifact on
  `127.0.0.1:18082`.
- Ran the queued `strict-suffix-copy-exact` repair through
  `scripts/select_prompt_profile_repair_experiment.py`.
- Stopped the endpoint after the run.

## Phase 2 - Result Recording

Status: completed

- Captured the strict `1/3` result and source output directory.
- Recorded the failure as `completed-no-promotion`.
- Kept promotion blocked because the successful case was only the invalid-tool
  refusal, not a valid Hermes tool-call case.
