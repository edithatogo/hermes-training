# Specification: Qwen3 Candidate Training and Tool-Call Gate

## Overview

Extend the Qwen3 4B local MLX lane beyond the smoke run, add a deterministic Hermes-local tool-call benchmark, and preserve an LM Studio GGUF validation path for practical Hermes runtimes.

## Requirements

- Run a local-safe Qwen3 candidate training pass from SSD-backed caches and artifacts.
- Evaluate the candidate on the 100-prompt Hermes-local set.
- Apply the response-collapse gate before any publication claim.
- Add and run a local BFCL-style tool-call benchmark covering JSON validity, argument correctness, invalid-tool handling, and multi-turn repair.
- Keep generated artifacts and benchmark outputs on `/Volumes/PortableSSD`.
- Document LM Studio validation commands for the existing Qwen3 GGUF artifact.

## Acceptance Criteria

- Candidate adapter trains without exceeding local memory.
- Candidate evaluation summary records training tokens, validation loss, latency, response gate, and tool-call score.
- Tool-call benchmark runner and suite are checked in; raw outputs stay under `$HERMES_EVAL_ROOT`.
- Runtime docs include the LM Studio smoke helper and exact Qwen3 GGUF path.

## Out of Scope

- Publishing the candidate adapter as a Hugging Face quality artifact.
- Downloading or running Qwen3.6/Hermes 4 large artifacts in this pass.
- Treating failed tool-call scores as model-quality success.
