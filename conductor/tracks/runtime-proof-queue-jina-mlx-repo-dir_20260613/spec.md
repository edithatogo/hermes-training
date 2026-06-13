# Specification: Runtime Proof Queue Jina MLX Repo Dir

## Overview

Jina MLX support-model proof commands should be directly executable after the
artifact is acquired. The command generator previously emitted a literal
`<repo-dir>` placeholder even though `scripts/run_jina_mlx_embedding_benchmark.py`
already resolves a deterministic SSD-backed default repo directory from
`HERMES_STORAGE_ROOT` or `/Volumes/PortableSSD`.

## Goals

- Remove the literal `--repo-dir .../<repo-dir>` placeholder from generated Jina MLX support-model commands.
- Keep `--local-files-only` in queued proof commands so blocked/unacquired artifacts fail closed.
- Make the command comment explain that first acquisition can remove `--local-files-only` after license/access checks.
- Regenerate and validate the runtime proof action queue.

## Acceptance Criteria

- Jina MLX text-matching command cards call `scripts/run_jina_mlx_embedding_benchmark.py` with `--task-type text-matching`.
- Jina MLX retrieval command cards call the same runner with `--task-type retrieval`.
- Generated Jina MLX command cards do not contain `<repo-dir>` or a literal `--repo-dir` override.
- The runtime proof action queue validates.

## Out Of Scope

- Downloading new Jina artifacts.
- Running a broader Jina benchmark.
- Changing mem0 defaults.
