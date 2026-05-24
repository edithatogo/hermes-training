# mem0 Training

This folder is for future embedding, reranker, and retriever fine-tuning recipes.

## Training Targets

| Target | Data shape | First framework | Notes |
|---|---|---|---|
| Dense embedder | contrastive triplets | sentence-transformers or Transformers | Use separate Qdrant collection per dimension. |
| Reranker | query, candidate, relevance label | Transformers or MLX wrapper | Start as post-retrieval reranker, not a vector-store replacement. |
| Late-interaction retriever | ColBERT-style pairs/triples | PyLate / ColBERT-compatible tooling | Requires separate index artifacts and retrieval API. |
| Extractor LLM | memory extraction instructions | Hermes chat SFT lane or small local LLM LoRA | Evaluate hallucination, duplicate, and unsafe-memory rates. |

## First Milestones

1. Keep `nomic-embed-text:latest` as rollback.
2. Build a larger contrastive triplet set from safe project docs and synthetic memory cases.
3. Run direct embedding benchmark against current and candidate embedders.
4. For dense embedders, create a candidate Qdrant collection and run mem0 add/search benchmark.
5. For rerankers, test on fixed candidate sets before live mem0 integration.
6. For ColBERT-style retrievers, expose `GET /health` and `POST /retrieve` before Hermes or mem0 integration.

## Non-Goals

- Do not fine-tune on private user memories for publishable artifacts.
- Do not use Hermes chat tool-call scores to approve an embedding model.
- Do not change the default mem0 config until a candidate beats the baseline and rollback is documented.

