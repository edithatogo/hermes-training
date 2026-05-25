# Specification: Nomic Expanded Retrieval and Reranker Replay

Run the same expanded mem0-oriented retrieval and reranking evaluation for
`nomic-embed-text:latest` that was previously run for BGE-M3, using the clean
SSD-backed Ollama root and preserving `nomic` as the rollback embedder unless a
larger promotion gate says otherwise.

Acceptance criteria:

- Use `/Volumes/PortableSSD/Ollama/mem0-clean-models` for Ollama model storage.
- Run `benchmarks/embeddings/memory_retrieval_expanded_suite.json` against
  `nomic-embed-text:latest`.
- Convert the ranked embedding results into a fixed candidate reranking suite.
- Replay `vector`, `score_plus_created_at_rank`,
  `score_plus_created_at_rank_close_margin`, and `lexical_overlap`.
- Store benchmark artifacts under `/Volumes/PortableSSD/hermes-evals`.
- Record a repo-local benchmark report, run-card entries, candidate radar
  update, reranking README update, and handoff update.
- Do not change `~/.mem0/config.json` or the live default collection.
