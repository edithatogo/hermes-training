# Specification: Colab Benchmark Environment Scale-Out

Prove that the Colab CLI lane can host a bounded official-benchmark
environment smoke on accelerator-backed remote compute while preserving the
project boundary between environment readiness and benchmark score claims.

Acceptance criteria:

- Add a Colab-safe benchmark environment bootstrap script that can install the
  benchmark package profile in the remote runtime and then call the existing
  official benchmark smoke harness.
- Keep TPU opt-in and document GPU-first use for CUDA benchmark packages.
- Route logs and summaries to `/Volumes/PortableSSD/hermes-evals/colab` through
  the dispatcher, with tracked markdown evidence under `reports/colab`.
- Update Colab scale-out documentation with the exact benchmark-environment
  command and the claim boundary.
- Validation passes without moving unrelated dirty model-radar files.

