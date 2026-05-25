# Plan: mem0 Cached Read Path Benchmark

## Phase 1: Cache Semantics

- [x] Task: add opt-in mem0 search-result caching to `scripts/mem0_read.py`.
- [x] Task: keep final reranking outside the cache.
- [x] Task: add unit coverage for cache miss, cache hit, disabled cache, and
  corrupt cache handling.

## Phase 2: Probe and Evidence

- [x] Task: extend the latency probe to pass cache options and report cache
  hit counts.
- [x] Task: run cold/warm live latency evidence with an output-local SSD cache.
- [x] Task: document the cached-read decision boundary.

## Phase 3: Validation

- [x] Task: run full unit and readiness gates.
- [x] Task: stop local services after validation.
- [x] Task: mark the track complete and push.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: live cached-read benchmark completed 10/10 read-only calls with 5
  cache hits, cold p50 `2.904s`, cache-hit p50 `0.000s`, no fallbacks, and
  singleton-only live-store results.
- Gaps: runtime integration remains a separate decision.
