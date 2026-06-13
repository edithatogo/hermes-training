# Specification: Runtime Proof Queue Strict Local Commands

## Overview

After endpoint command cards were tightened, MLX local runtime proof and
prompt-profile repair command cards still omitted `--require-no-extra-tool-text`.
Those commands should use the same strict Hermes evidence boundary.

## Goals

- Add strict no-extra-tool-text scoring to MLX runtime proof commands.
- Add strict no-extra-tool-text scoring to prompt-profile repair commands.
- Keep raw response preservation and existing score-only normalizer options intact.
- Regenerate and validate the runtime proof action queue.

## Acceptance Criteria

- `mac-mlx` runtime proof command cards include `--require-no-extra-tool-text`.
- `prompt-profile-repair` command cards include `--require-no-extra-tool-text`.
- Unit coverage locks both command shapes.
- `scripts/validate_runtime_proof_action_queue.py` and hub readiness validation pass.

## Out Of Scope

- Running local MLX pilots.
- Changing prompt profiles.
- Promoting any model.
