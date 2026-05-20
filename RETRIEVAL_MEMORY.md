# Retrieval and Hermes Memory Lane

This lane is for retrieval, reranking, and Hermes memory/RAG work. It is intentionally separate from chat SFT so the data, metrics, serving shape, and publication rules do not blur together.

## Lane Rule

- Chat adapters are judged on assistant behavior, tool calls, and chat benchmarks.
- Retrieval models are judged on retrieval objectives, memory grounding, and indexed corpora.
- Do not use chat promotion gates to approve retrievers.

## Canonical Decisions

- Candidate models: LFM2-ColBERT, BGE-M3, Jina embeddings v4, Qwen3-Embedding-4B, and Qwen3-Reranker-4B.
- Training data: contrastive JSONL triplets with anchor, positive, and negative examples.
- Hermes evals: grounded memory recall, doc QA, multi-hop retrieval, preference updates, recency conflicts, source attribution, and distractor resistance.
- Benchmark shape: `mteb run` for standard embedding runs, with retrieval-only task selection.
- Local store: SSD-backed FAISS for dense vectors plus SQLite metadata; ColBERT-style retrievers may use their own index artifacts but must expose the same API.
- Serving shape: a small retriever service with `GET /health` and `POST /retrieve`.

## Retriever API Shape

Hermes should call retrieval as a separate tool/service step. The retriever returns citation-ready ids and scored passages, not a chat response.

Required fields in the retrieval response:

- `doc_id`
- `chunk_id`
- `source_id`
- `score`
- `citation`
- `index_id`
- `model_id`

## Hermes Memory Scenarios

The evaluation set should cover:

1. Direct fact recall from prior memory.
2. Document-grounded answers with citations.
3. Multi-hop retrieval across more than one source.
4. Preference updates where the latest memory overrides the older one.
5. Recency conflicts.
6. Source attribution.
7. Tool-state recall.
8. Distractor resistance.

## Publication Checklist

Retriever cards should publish:

- model family and revision
- retriever role
- index type and rebuild command
- corpus provenance and license notes
- retrieval metrics such as Recall@k, nDCG@10, and MRR@10
- latency and throughput notes
- known limitations

Retriever cards should not publish:

- raw private corpora
- user prompts
- proprietary embeddings
- chat SFT claims

The card, corpus digest, and index hash must agree with the published numbers.
