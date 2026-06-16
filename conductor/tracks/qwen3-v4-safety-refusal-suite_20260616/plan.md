# Plan: Qwen3 v4 Safety/Refusal Suite

## Phase 1 - Queue And Manifest

- [x] Task: correct the official-candidate queue command from stale `--config`
  to `--suite`.
- [x] Task: add `scripts/materialize_safety_refusal_suite.py`.
- [x] Task: materialize the pinned JSON and Markdown suite manifest.

## Phase 2 - Validation

- [x] Task: validate the suite through `run_tool_call_benchmark.py --dry-run`.
- [x] Task: add `scripts/validate_safety_refusal_suite.py`.
- [x] Task: add focused unit tests for the manifest materializer and validator.
- [x] Task: wire the validator into `scripts/validate_readiness.py`.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: the suite has 8 cases, including 5 invalid/disallowed-tool refusal
  cases with forbidden-marker checks, plus the control categories required by
  the scorer. The queue command now points at the pinned manifest with `--suite`
  and an SSD-backed output root.
- Remaining gap: the suite has not been scored against the Qwen3 v4 adapter.
- Decision: complete this manifest/setup track. Do not mark `safety-refusal`
  coverage present until scored outputs are ingested.
