# Specification: Qwen3.5 2B MLX Smoke

Prove the Qwen3.5 2B candidate can be acquired to the SSD-backed Hugging Face
cache and loaded through the direct MLX loglikelihood smoke harness.

Acceptance criteria:

- Run a bounded one-case loglikelihood smoke for `Qwen/Qwen3.5-2B`.
- Store raw outputs under `/Volumes/PortableSSD/hermes-evals`.
- Track a markdown report under `reports/benchmark/mlx-loglikelihood`.
- Update the runtime proof queue and candidate notes from blocked preflight to
  completed runtime proof.
- Keep the result classified as runtime/load proof only, not a quality
  benchmark or adapter promotion.
- Validation passes.

