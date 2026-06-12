# Qwen Retrieval Current Release Scan

This scan updates the Hermes retrieval lane with the official Qwen models
dedicated to embeddings and reranking:

- `Qwen/Qwen3-Embedding-4B`
- `Qwen/Qwen3-Reranker-4B`

## What Changed

- Qwen3 Embedding now provides an official 4B retrieval model for embedding and
  ranking tasks.
- Qwen3 Reranker now provides an official 4B reranking model that can sit after
  dense retrieval.
- These models should be treated as Hermes memory and RAG helpers, not chat SFT
  targets.

## Practical Reading

- Compare the embedding model against BGE-M3 and Jina embeddings for Hermes
  memory.
- Use the reranker after candidate retrieval to tighten precision.
- Keep the retrieval lane separate from chat adapter training.

## Evidence Notes

Verified from current Hugging Face model pages:

- [Qwen3 Embedding-4B](https://huggingface.co/Qwen/Qwen3-Embedding-4B)
- [Qwen3 Reranker-4B](https://huggingface.co/Qwen/Qwen3-Reranker-4B)

## Result

The radar now includes the official Qwen retrieval helpers relevant to Hermes
memory and RAG.
