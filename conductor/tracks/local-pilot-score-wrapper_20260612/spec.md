# Specification: Local Pilot Score Wrapper

Add a narrow local pilot scoring mode for prompt-repair experiments where a
generation prefill should be treated as part of the response contract during
scoring, while preserving the raw model output.

Acceptance criteria:

- Add `--score-prefix` and `--score-suffix` to
  `scripts/run_local_pilot_benchmark.py`.
- Preserve raw generated `response` and record `scored_response` only when it
  differs.
- Add unit coverage for wrapper construction.
- Run a bounded Qwen3.5 0.8B BFCL-style wrapper retry.
- Track the result as pass or fail without changing promotion status.
- Validation passes.
