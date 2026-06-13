# Specification: Qwen3 V4 PEFT NGC Cloud Function Scorecard

## Overview

Identify the viable NVIDIA NGC execution surface for a persistent Qwen3 v4 PEFT
selected-task `lm_eval[hf]` scorecard and fail closed until auth, entitlement,
container, and result persistence are proven.

## Acceptance Criteria

- Record the installed NGC CLI command surface.
- Confirm whether `ngc batch` exists in this environment.
- Identify the likely task execution route if one is available.
- Record current auth/org/team/container/quota blockers.
- Do not submit NGC tasks or create cloud functions while credentials and
  entitlements are absent.

## Out Of Scope

- Storing NGC API keys in tracked files.
- Creating NGC registry images or cloud-function tasks without explicit
  confirmation.
- Making benchmark claims from unexecuted NGC templates.
