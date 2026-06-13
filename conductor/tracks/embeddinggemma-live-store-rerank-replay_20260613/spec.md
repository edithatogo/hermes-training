# Spec

## Problem

EmbeddingGemma copied live-store replay retrieved the current default top memory
inside candidate results for every comparable query, but top-1 match was only
`0.200`. The next useful question is whether an existing opt-in rerank strategy
can restore default top-1 ordering on the same bounded evidence.

## Scope

- Read the private copied live-store replay JSONL artifacts from the SSD.
- Evaluate existing no-download rerank strategies over candidate results.
- Commit only redacted hash-level metrics and a redacted report.
- Keep `~/.mem0/config.json`, `mem0_nomic_768`, and the EmbeddingGemma opt-in
  profile unchanged.

## Non-Goals

- Publishing raw memory text.
- Promoting EmbeddingGemma to the default mem0 embedder.
- Training a new reranker.
- Uploading private mem0 artifacts to cloud runtimes.

## Acceptance

- A repeatable offline replay script exists.
- Focused tests prove the report excludes raw memory text.
- A committed report records whether any existing strategy restores top-1.
- Candidate docs and track status reflect the result.
