# Specification: Hermes Shortlist Crystallization

## Overview

The Hermes lane needs a frozen shortlist so the repo clearly separates models
that are realistic local training candidates from baseline, runtime, helper,
and watchlist-only lanes.

This track turns the current Hermes-related radar into an explicit decision
surface for:

- the Hermes training shortlist
- the Hermes baseline/teacher set
- runtime comparison lanes
- helper/support-only lanes
- watchlist-only models that are not ready for promotion

## Scope

- Classify the Hermes-related candidates already present in `MODEL_CANDIDATES.yaml`.
- Align `FUTURE_MODELS.md` and `HANDOFF.md` with the crystallized Hermes
  shortlist.
- Preserve the distinction between trainable targets and runtime-only
  comparison lanes.
- Keep the Mac/MLX lane first, but retain Ollama, LM Studio, and GGUF as valid
  runtime proofs where they are stronger.

## Out Of Scope

- No training runs in this slice.
- No publication or push to remote.
- No broad radar expansion beyond the Hermes family and its direct baselines.

## Acceptance Criteria

- The Hermes shortlist is clearly tagged in the radar and handoff docs.
- The repo says which Hermes models are training candidates and which are only
  runtime or teacher lanes.
- Watchlist-only Hermes-adjacent models remain explicitly non-promotion items.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: this is a scope-frozen documentation and candidate-classification
  slice.
- Remaining gap: runtime proof and any fine-tuning remain separate tracks.
