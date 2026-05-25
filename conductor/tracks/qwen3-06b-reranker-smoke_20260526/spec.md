# Specification: Qwen3 0.6B Reranker Smoke

Validate a smaller learned reranker before attempting heavier Qwen3 4B or
specialist MLX reranker paths.

Acceptance criteria:

- Verify the target reranker artifact exists and is compatible with the current
  local harness.
- Avoid the nonexistent `Qwen/Qwen3-Reranker-0.6B-ONNX` repo id and use the
  real lightweight candidate.
- Run the learned reranker against the expanded fixed mem0 candidate suite and
  the BGE/nomic embedding-derived suites when feasible.
- Store benchmark outputs under `/Volumes/PortableSSD/hermes-evals`.
- Record benchmark reports, run cards, candidate radar/queue updates, and
  handoff updates.
- Do not alter `~/.mem0/config.json` or any live mem0 defaults.
