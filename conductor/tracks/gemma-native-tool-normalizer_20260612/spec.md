# Spec: Gemma Native Tool Normalizer Analysis

## Problem

Gemma 4 E4B MLX emitted native thought/tool fragments rather than strict Hermes
tool-call JSON. The strict gate correctly failed, but the project also needs to
know whether a runtime adapter could recover semantic tool intent for helper or
comparison use.

## Scope

- Add score-only Gemma native payload conversion for local pilot analysis.
- Preserve strict raw responses and strict promotion semantics.
- Add unit coverage for truncated Gemma native tool fragments and refusal text.
- Run the Gemma 4 E4B BFCL-style pilot with the score-only normalizer.
- Document the result and update handoff guidance.

## Out Of Scope

- No strict benchmark promotion.
- No endpoint proxy mutation.
- No training data generation from normalized outputs.
- No publication claim beyond runtime-adapter analysis.

## Acceptance Criteria

- Strict scorer behavior remains unchanged by default.
- The local pilot runner records `score_normalizer`.
- Normalized scoring is opt-in and preserves raw output.
- Unit tests and repo readiness checks pass.
