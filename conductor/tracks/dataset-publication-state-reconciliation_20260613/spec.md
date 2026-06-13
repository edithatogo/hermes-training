# Spec

## Problem

The Qwen3 v4 cleaned synthetic-only dataset has a live publication record and a
public Hugging Face dataset repo, but several operator-facing documents still
said dataset publication was blocked pending approval. That stale state can make
future agents repeat publication work or report the wrong blocker.

## Scope

- Verify the current Hugging Face dataset repo state.
- Update handoff and publication docs from blocked to published where
  appropriate.
- Preserve the narrow benchmark and model-claim caveats.
- Record the reconciliation in Conductor.

## Non-Goals

- Uploading new dataset files.
- Changing model or adapter publication state.
- Expanding benchmark claims beyond recorded evidence.

## Acceptance

- The docs identify the live dataset URL and remote SHA.
- The roadmap gate no longer lists dataset approval as an open blocker.
- Conductor metadata and registry are consistent.
- Readiness validation passes before push.
