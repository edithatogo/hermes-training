# Specification: Granite 4.1 3B Native-Normalized Local Pilot

## Overview

Granite 4.1 3B is a practical Mac-local instruction model candidate, but the
repo needs to know whether it can contribute semantic tool intent for Hermes
style workflows without being promoted as a strict tool-call model.

This track records two things:

1. the direct MLX load and local pilot behavior, and
2. the effect of a score-only native tool-call normalizer on the BFCL-style
   local pilot.

## Scope

- Add the Granite native function payload normalizer used only for scoring.
- Preserve raw output and strict promotion semantics.
- Capture the raw strict pilot and the score-normalized strict pilot.
- Update the model radar, proof queue, and handoff notes with the result.
- Add a report artifact under `reports/benchmark/local-pilots`.

## Out Of Scope

- No strict Hermes promotion.
- No endpoint mutation or proxy behavior changes.
- No adapter publication claim.
- No training claim.

## Acceptance Criteria

- The repository records the Granite runtime-adapter result in a track.
- The model radar reflects Granite 4.1 3B as runtime-proven but still strict-
  format blocked.
- The proof queue and handoff note the native-normalized pass rate.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the MLX smoke passed, the raw strict pilot exposed the remaining
  Hermes-format gap, and the native score-only normalizer improved the strict
  pilot from `1/3` to `2/3` without mutating raw output.
- Remaining gap: the parallel ticket-routing case still does not emit a fully
  strict Hermes tool call.
