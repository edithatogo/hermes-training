# Specification: Tiny MLX BFCL Role Gate

Compare the newly load-proven tiny MLX candidates on the same BFCL-style local
pilot before making any Hermes tool-call role claim.

Acceptance criteria:

- Run `benchmarks/endpoint_pilots/bfcl_pilot.json` through local MLX generation
  for MiniCPM5 1B, Qwen3.5 0.8B, and Qwen3.5 2B.
- Store raw outputs under `/Volumes/PortableSSD/hermes-evals`.
- Track a comparison report under `reports/benchmark/local-pilots`.
- Update handoff and candidate notes if the role gate changes promotion status.
- Keep failures fail-closed.
- Validation passes.
