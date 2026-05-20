# Spec: Retrieval and Hermes Memory Model Lane

## Goal

Separate Hermes memory/RAG model work from chat SFT so embedding, reranking, and ColBERT-style models are evaluated with the right data and benchmarks.

## Requirements

- Retrieval models must not use chat adapter promotion gates.
- Candidate models include LFM2-ColBERT, BGE-M3, Jina embeddings, Qwen3-Embedding-4B, and Qwen3-Reranker-4B.
- Training, if attempted, must use contrastive or retrieval-specific objectives.
- Evaluation must include MTEB or task-specific retrieval checks plus Hermes memory scenarios.
- Contracts must define the retrieval triplet JSONL, Hermes memory/RAG scenarios, benchmark command shape, local vector store, retriever serving shape, and retriever publication guidance.
- Health target: `>= 9.5 / 10`.

## Acceptance Criteria

- Retrieval lane exists in model radar and applications docs.
- Benchmark plan distinguishes retrieval from chat SFT.
- Runtime/package docs identify how Hermes should call retrieval separately from chat models.
- A future dedicated retrieval repo can be created from this spec without changing chat tracks.
