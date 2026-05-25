# Specification: mem0 MLX BGE Daily-Use Latency Probe

Run the next opt-in mem0 gate for
`flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` after fixed-suite,
expanded-suite, guarded-read, and isolated-fixture proofs.

Acceptance criteria:

- Add `mlx-bge` support to the daily-use read latency probe.
- Keep the probe read-only and leave default mem0 configuration unchanged.
- Bound model load/fetch stalls so daily-use probes can fail closed.
- Record the first latency result and update the mem0 candidate queue/index.
- Keep MLX BGE opt-in until a broader cold/warm multi-query proof exists.
