# Plan: mem0 MLX BGE Daily-Use Latency Probe

## Phase 1: Harness Support

- [x] Task: add `mlx-bge` to `scripts/run_mem0_read_latency_probe.py`.
- [x] Task: pass `mlx_max_length` through to the guarded read wrapper.
- [x] Task: add child-process read execution so wall-clock timeouts can kill
  artifact fetch or model-load stalls.
- [x] Task: cover the new mode and subprocess command surface in tests.

## Phase 2: Probe and Evidence

- [x] Task: run the initial daily-use probe with vector fallback enabled.
- [x] Task: record the unbounded in-process stall and bounded subprocess result.
- [x] Task: update the mem0 benchmark index and candidate queue.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: `mlx-bge` probe selection is tested; bounded subprocess execution
  completed a cache-hit read in 4.610s total with 0.059s rerank latency; no
  mem0 defaults were changed.
- Remaining gap: this is one cache-hit query. Default integration still needs a
  broader cold/warm multi-query latency proof.
