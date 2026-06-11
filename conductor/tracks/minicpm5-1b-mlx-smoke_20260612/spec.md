# Specification: MiniCPM5 1B MLX Smoke

Prove the official MiniCPM5 1B MLX package can be acquired to the SSD-backed
Hugging Face cache and scored through the direct MLX loglikelihood smoke
harness.

Acceptance criteria:

- Verify exact Hugging Face IDs for MiniCPM5 1B base, MLX, GGUF, and SFT
  packages.
- Add the MLX package to `MODEL_CANDIDATES.yaml`.
- Run a bounded one-case direct MLX loglikelihood smoke.
- Store raw outputs under `/Volumes/PortableSSD/hermes-evals`.
- Track a markdown report under `reports/benchmark/mlx-loglikelihood`.
- Update the runtime proof queue and handoff notes.
- Keep the result classified as runtime/load proof only.
- Validation passes.
