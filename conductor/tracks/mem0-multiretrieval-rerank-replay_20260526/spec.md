# Spec: mem0 Multi-Result Rerank Replay Harness

## Goal

Provide a non-invasive multi-result reranking comparison path while the live
default mem0 store only returns singleton results.

## Requirements

- Reuse existing fixed candidate suites and ranking metrics.
- Exercise the same read-only wrapper path used by live mem0 reranking.
- Support heuristic strategies and the warm Qwen3 reranker service.
- Write benchmark outputs under the SSD-backed `HERMES_EVAL_ROOT`.
- Do not write to the live mem0 store or change `~/.mem0/config.json`.
- Document results and promotion gates.

## Non-Goals

- Do not create or mutate live memories.
- Do not promote a default reranker from replay alone.
- Do not validate the ONNX/Transformers.js bridge in this track.
