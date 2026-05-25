# Spec: mem0 Isolated Fixture Rerank Proof

## Goal

Validate reranking against real mem0 add/search behavior without contaminating
the default live `cmd` memory namespace.

This track uses namespace isolation only. The stronger follow-on gate uses
`MEM0_CONFIG_PATH` plus an output-local Qdrant path.

## Requirements

- Use a dedicated non-sensitive fixture namespace.
- Keep cleanup enabled and report cleanup count.
- Compare raw vector ordering, close-margin reranking, and warm Qwen3 0.6B
  reranking.
- Keep all model caches and benchmark outputs on `/Volumes/PortableSSD`.
- Do not change `~/.mem0/config.json`.

## Non-Goals

- Do not promote a global mem0 default.
- Do not publish fixture memories.
- Do not validate the ONNX bridge in this track.
