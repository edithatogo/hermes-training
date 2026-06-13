# Specification: Runtime Proof Queue Strict Endpoint Commands

## Overview

Endpoint runtime proof command cards used the BFCL-style pilot suite but did not
pass `--require-no-extra-tool-text`. That made the generated commands less strict
than the Hermes promotion boundary for tool-call evidence.

## Goals

- Add `--require-no-extra-tool-text` to generated endpoint pilot commands.
- Keep both GGUF and non-GGUF endpoint candidates on the bounded endpoint pilot path.
- Preserve existing artifact hints and SSD storage guidance.
- Regenerate and validate the runtime proof action queue.

## Acceptance Criteria

- GGUF endpoint command cards include `--require-no-extra-tool-text`.
- Non-GGUF endpoint command cards include `--require-no-extra-tool-text`.
- Unit coverage locks both command shapes.
- `scripts/validate_runtime_proof_action_queue.py` and hub readiness validation pass.

## Out Of Scope

- Running endpoint pilots.
- Changing candidate ranking.
- Promoting any model.
