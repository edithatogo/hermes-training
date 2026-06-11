# Spec: Local Pilot Strict Tool Text Gate

## Problem

The lightweight BFCL-style pilot could count a response as passing when the
expected tool-call JSON was present but extra thought text surrounded it. That
is useful as parsed-tool diagnostic evidence, but not sufficient for Hermes
strict-format claims.

## Scope

- Add an opt-in `--require-no-extra-tool-text` flag to endpoint and local pilot
  runners.
- Preserve previous permissive parsed-tool behavior by default.
- Record leftover text and `no_extra_text_ok` in result rows.
- Add unit coverage for permissive versus no-extra scoring.
- Re-run the Gemma 4 E4B profile under the stricter gate.

## Out Of Scope

- No change to existing historical pilot scores.
- No promotion of Gemma profile results.
- No endpoint proxy mutation.

## Acceptance Criteria

- Existing callers are backward compatible.
- Strict no-extra scoring fails responses with leftover text around tool calls.
- Summary output records when the strict flag was enabled.
- Full validation passes.
