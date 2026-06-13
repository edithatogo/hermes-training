# Specification: Runtime Proof Queue Acquisition Priority

## Overview

The runtime proof queue used active parameter count to classify MoE candidates.
That is useful for inference feasibility, but it can hide acquisition and storage
risk: an `80B total / 3B active` package may still require a large artifact
download, cache footprint, and conversion path.

## Goals

- Preserve active-parameter size buckets for feasibility notes.
- Add acquisition/storage ordering based on total parameter count.
- Sort immediate Mac runtime proofs so small dense and small packaged candidates are tried before huge-total MoE packages.
- Keep lane ordering unchanged; this track only changes ordering inside comparable lanes.

## Acceptance Criteria

- `scripts/build_runtime_proof_action_queue.py` computes a separate acquisition-size order.
- Runtime proof priorities sort by lane, then acquisition-size order, then active/effective size, then candidate ID.
- Unit coverage verifies a small dense local proof sorts ahead of an `80B total / 3B active` proof candidate.
- Regenerated queue reports show smaller Mac-local candidates before huge-total packages.
- Queue validation and hub readiness validation pass.

## Out Of Scope

- Downloading, converting, or running new model artifacts.
- Reclassifying model quality or promotion status.
- Changing cloud/offload blockers.
