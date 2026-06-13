# Specification: Prompt/Profile Repair Queue

## Overview

The all-candidate coverage report already identifies Hermes candidates that are
load-proven or otherwise worth keeping, but blocked by strict tool-call
formatting or empty strict-prompt output. Those candidates need an explicit
repair queue so follow-on work targets prompt/profile fixes before more
training, downloads, or remote execution.

## Goals

- Extract Hermes candidates whose blocker is strict tool-call formatting failure
  or empty/no-content strict-prompt generation.
- Generate no-download rerun commands that reuse existing local artifacts or
  endpoints.
- Require `--require-no-extra-tool-text` in every queued strict BFCL pilot.
- Keep raw model outputs distinct from any score-only normalizer or helper.
- Add a deterministic validator and wire it into hub readiness.

## Acceptance Criteria

- The generated JSON and Markdown reports exist under
  `reports/benchmark/coverage/prompt-profile-repair-queue-20260614.*`.
- The validator fails when generated reports are stale or command strictness is
  missing.
- Focused unit tests cover filtering, local/endpoint command shapes, and stale
  report detection.
- `scripts/validate_readiness.py` runs the prompt/profile repair queue
  validator.
- Conductor consistency and full readiness pass.

## Out Of Scope

- Running local benchmark pilots.
- Changing model prompt profiles.
- Promoting any candidate to Hermes default use.
- Downloading or acquiring additional artifacts.
