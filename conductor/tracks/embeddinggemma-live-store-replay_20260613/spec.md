# EmbeddingGemma Copied Live-Store Replay

## Overview

The EmbeddingGemma opt-in profile is proven, but it is still not eligible for a
default mem0 switch until it has been tested against representative memories
copied from the current live default. This track exports a bounded, redacted
sample from the default `mem0_nomic_768` store, re-embeds it into the
`mem0_embeddinggemma_300m_768` candidate collection through the resilient
llama.cpp proxy, compares retrieval for representative queries, and records a
rollback decision.

## Functional Requirements

- Read from the current default mem0 config without editing it.
- Export only a bounded sample and write artifacts under `/Volumes/PortableSSD`.
- Avoid committing raw memory content to Git.
- Re-embed copied memories into the candidate EmbeddingGemma profile with
  `infer=False` so extraction does not rewrite facts.
- Compare default and candidate retrieval for a bounded query set.
- Record aggregate metrics, blockers, and rollback state in a report.

## Non-Functional Requirements

- The live default collection `mem0_nomic_768` must remain intact.
- The candidate profile must use `mem0_embeddinggemma_300m_768` or a run-scoped
  derivative, not the live default collection.
- Server processes and ports must stop after the run.
- Reports committed to Git must summarize results and paths, not disclose raw
  memory text.

## Acceptance Criteria

- Live-store export completes or documents a precise blocker.
- Candidate re-embed completes through the resilient proxy or documents a
  precise blocker.
- Comparison report states whether EmbeddingGemma matches, beats, or regresses
  against the current default on the copied sample.
- Focused tests and readiness validation pass.
- The Conductor track status matches the evidence.

## Out Of Scope

- Editing `~/.mem0/config.json`.
- Deleting or modifying live default memories.
- Publishing private memory contents.
- Making EmbeddingGemma the default in this track.
