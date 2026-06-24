# Specification: Qwen3 v4 BFCL Completion-Suffix Runtime Bridge

## Overview

The BFCL clean rerun cleared upstream endpoint/proxy errors but still produced
blank `/v1/completions` outputs. This track adds a narrow runtime bridge for the
next BFCL attempt: append a generation-only completion prompt suffix so the
model starts inside the expected `<tool_call>` envelope.

## Requirements

- Keep the existing BFCL zero-score repair track active as the owning source
  track.
- Keep all raw BFCL outputs and logs under `/Volumes/PortableSSD`.
- Add the completion suffix only to `/v1/completions` payloads, not chat
  completions.
- Preserve BFCL scoring semantics: the next score can only be interpreted after
  a bounded rerun records zero upstream-error rows and zero blank-output rows.
- Keep this as runtime-bridge evidence only; do not publish model weights or
  model-quality claims from the diagnostic.

## Acceptance Criteria

- `scripts/openai_normalizing_proxy.py` supports a configurable
  `--completion-prompt-suffix`.
- Unit tests cover string and list completion prompts.
- A validator-backed diagnostic report records the existing blank-output
  evidence and the next gated rerun command boundary.
- `scripts/validate_readiness.py` includes the diagnostic validator.
- GitHub is pushed after focused tests pass.

## Out Of Scope

- Full official BFCL leaderboard claims.
- Adapter retraining or model-weight publication.
- Native architecture changes for ColBERT, llama.cpp, or BFCL scoring internals.
