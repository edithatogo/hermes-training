# Release Decision: Qwen3 4B Strict Tool-Call V6 Free-Text Copy

Date: 2026-06-13

## Decision

Promote v6 iteration 125 for local Hermes strict tool-call integration.

Do not publish externally yet.

## Rationale

- Iteration 125 passes the held-out strict local tool-call suite at `1.000`.
- Iteration 125 passes the mirrored regression suite at `1.000`.
- Final iteration 170 is rejected because it regresses to `0.875` on the
  held-out lab-order argument case.
- Repo-native BFCL-style, IFEval-style, and coding pilots remain pilot-only
  and each score `0.667` for iteration 125.
- Bounded official IFEval pilot scores prompt strict `0.720` at limit 25,
  which supports keeping broad instruction-following claims out of scope.

## Required Before External Publication

1. Finalize the Hugging Face model card.
2. Record explicit human approval for public adapter upload.
3. Decide whether the cleaned synthetic-only v6 dataset should also be
   published or kept as local evidence.
4. Re-run the publication bundle validator after any wording changes.
