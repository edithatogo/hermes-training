# Spec: mem0 Read UX Latency Probe

## Goal

Measure the agent-facing latency of the guarded mem0 read wrapper over repeated
Hermes-agent-like memory lookups before any runtime wiring decision.

## Requirements

- Reuse `scripts/mem0_read.py` rather than duplicating reranker behavior.
- Run multiple read queries and record p50/p95 total, search, and rerank
  latency.
- Record singleton, empty, and multi-result counts so quality claims do not
  overstate live-store evidence.
- Write benchmark artifacts under the SSD-backed eval root.
- Keep the probe read-only and avoid mutating mem0 config or collections.
- Document the decision boundary for Hermes-agent integration.

## Non-Goals

- Do not wire the wrapper into Hermes runtime in this track.
- Do not change `~/.mem0/config.json`.
- Do not promote Qwen3 as a default reranker.
