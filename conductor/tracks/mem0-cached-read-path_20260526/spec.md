# Spec: mem0 Cached Read Path Benchmark

## Goal

Add and benchmark an opt-in cache for repeated guarded mem0 reads so Hermes
agents can use an explicit or cached memory-read tool without changing mem0
defaults.

## Requirements

- Cache only the successful `mem0 search` result, not final reranker output.
- Rerank on every invocation so mode, fallback, and Qwen behavior remain
  request-specific.
- Keep caching opt-in with a TTL; default behavior must remain uncached.
- Store cache files on SSD-backed paths when used by benchmarks.
- Record cache hit counts, cold/warm latency, and singleton/multi-result counts.
- Preserve read-only behavior and avoid changing `~/.mem0/config.json` or
  `mem0_nomic_768`.

## Non-Goals

- Do not wire the cached path into Hermes runtime automatically.
- Do not cache failures or reranker fallback decisions.
- Do not promote Qwen3 as the live default reranker.
