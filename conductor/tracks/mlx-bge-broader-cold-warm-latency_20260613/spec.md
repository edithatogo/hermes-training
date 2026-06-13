# Spec

## Problem

`flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` is the strongest practical
MLX cross-encoder reranker candidate, but the current queue still limits it to
explicit opt-in use until a broader cold/warm daily-use latency proof exists.

## Scope

- Run `scripts/run_mem0_read_latency_probe.py` in `mlx-bge` mode over the
  standard five mem0 operational queries.
- Use child-process reads and a hard wall timeout so model-load or artifact
  stalls fail closed.
- Use a shared cache path and two iterations to capture cold and cache-hit
  behavior.
- Commit a redacted/aggregate report only; no raw mem0 output.
- Keep `~/.mem0/config.json`, `mem0_nomic_768`, and Hermes defaults unchanged.

## Non-Goals

- Promoting MLX BGE as an automatic/default read path.
- Replacing the current nomic embedder or close-margin default wrapper.
- Uploading private mem0 state or raw memory text.

## Acceptance

- Probe completes or fails closed with an explicit report.
- Report records case count, fallback count, input-count shape, cold/cache
  latency, and opt-in decision.
- mem0 candidate queue and benchmark docs reflect the result.
- Readiness and focused tests pass before publication.
