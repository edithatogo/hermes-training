# Spec: Qwen3.6 Runtime Proof and Qwen3.7 Hosted-Preview Watchlist

## Overview

Create a concrete next track that proves the Qwen3.6 and Hermes 4 runtime paths using only SSD-backed artifacts and documented local endpoints, while keeping Qwen3.7 in hosted-preview watchlist status only. This pass must not depend on large downloads.

## Requirements

- Verify the current Qwen3.6 runtime path with an existing local artifact, endpoint, or documented fallback. Do not fetch new large weights as part of this track.
- Verify the current Hermes 4 runtime path with an existing local artifact, endpoint, or documented fallback. Do not fetch new large weights as part of this track.
- Record exact command lines, endpoints, and smoke outcomes in SSD-backed notes or run cards.
- Keep all generated documentation, notes, and artifacts on `/Volumes/PortableSSD`.
- Update the model radar and runtime docs so Qwen3.7 remains a hosted-preview watchlist item only.
- Make the next-step policy concrete enough that future runtime work can start from this track without re-litigating the download guardrails.

## Acceptance Criteria

- The track directory contains `spec.md`, `plan.md`, `index.md`, and `metadata.json`.
- The runtime docs clearly separate Qwen3.6/Hermes 4 runtime proof from Qwen3.7 hosted-preview watchlist status.
- No large model downloads are required or introduced by this track.
- The conductor registry lists the new track.
- All referenced output paths stay SSD-first.

## Out of Scope

- Fine-tuning, merging, or publishing adapters.
- Downloading large Qwen3.6, Hermes 4, or Qwen3.7 artifacts as part of this track.
- Benchmark claims beyond runtime smoke and watchlist classification.
