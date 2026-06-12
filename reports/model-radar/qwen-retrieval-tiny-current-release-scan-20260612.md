# Qwen Retrieval Tiny Current Release Scan

This scan updates the Hermes retrieval lane with the official Qwen 0.6B
embedding and reranking models:

- `Qwen/Qwen3-Embedding-0.6B`
- `Qwen/Qwen3-Reranker-0.6B`

## What Changed

- Qwen3 Embedding 0.6B is the smaller official retrieval model and a better
  fit for a 32GB Mac than the 4B embedding model.
- Qwen3 Reranker 0.6B is the smaller official reranker and already has local
  benchmark evidence in the mem0 work.
- These models should be treated as Hermes memory and RAG helpers, not chat SFT
  targets.

## Practical Reading

- Prefer the 0.6B pair for the initial Hermes memory stack on Mac.
- Compare the 0.6B embedder against BGE-M3 and Jina embeddings if you need a
  retrieval baseline.
- Keep the 4B pair as a heavier comparison path only.

## Evidence Notes

Verified from current Hugging Face model pages:

- [Qwen3 Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)
- [Qwen3 Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B)

## Result

The radar now includes the official Qwen retrieval pair that best fits the
MacBook Pro M1 Max / 32GB Hermes memory lane.
