# mem0 Embedding and Reranker Promotion Execution

## Overview

Execute the mem0 model roadmap for embeddings, retrieval, reranking, and read UX. This track keeps `BAAI/bge-m3` as the current baseline while testing stronger candidates from the roadmap and scan report under repeatable local and offloaded workflows.

## Scope

- Preserve `BAAI/bge-m3` as the current mem0 retrieval baseline until a challenger wins on quality, latency, footprint, and migration cost.
- Evaluate current challenger lanes:
  - `jinaai/jina-embeddings-v5-omni-small`
  - `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx`
  - `google/embeddinggemma-300m`
  - `Qwen/Qwen3-Embedding-4B`
  - `Qwen/Qwen3-Reranker-4B`
  - Qwen3 0.6B reranker only after prompt/metadata work and bounded ONNX/CoreML proof
- Expand cold/warm latency, quality, and fixture benchmarks for mem0 read paths.
- Use Colab for heavier embedding/reranker benchmark sweeps where it materially reduces local load.
- Gate default-switch and collection migration decisions with explicit rollback steps.

## Out of Scope

- Mutating live mem0 defaults without explicit approval.
- Rebuilding production memory collections before migration validation.
- Treating reranker demos as default read-path approval.
- Uploading private memory fixtures to external services.

## Acceptance Criteria

- Each embedding and reranker candidate has a current benchmark state and role.
- Cold and warm latency results are captured for baseline and challenger paths.
- Quality comparisons use isolated fixtures plus realistic multi-result replay where available.
- Any proposed default switch includes migration, rollback, storage, and runtime compatibility notes.
- Private data remains local or synthetic; cloud jobs use sanitized fixtures only.

## Health Target

This track should not be marked complete below health 9.5. The final state must make the next mem0 default decision executable and reversible.
