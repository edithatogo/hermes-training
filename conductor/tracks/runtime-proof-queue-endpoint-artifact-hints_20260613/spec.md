# Specification: Runtime Proof Queue Endpoint Artifact Hints

## Overview

Endpoint-based local runtime proofs can be backed by GGUF, GPTQ, MLX-served, or
other local artifacts depending on the runtime. The queue command comment
previously always said to acquire a GGUF artifact for LM Studio/Ollama-style
endpoint pilots, which was inaccurate for candidates such as
`openbmb/MiniCPM-V-4.6-GPTQ`.

## Goals

- Keep the endpoint pilot harness for endpoint-served local candidates.
- Use a GGUF-specific acquisition hint only when the candidate itself or runtime text indicates GGUF.
- Use a runtime-neutral local-artifact hint for other endpoint candidates.
- Regenerate and validate the runtime proof action queue.

## Acceptance Criteria

- Non-GGUF `mac-lmstudio` candidates do not render a GGUF-only acquisition hint.
- GGUF candidates retain the GGUF-specific hint.
- Unit coverage locks the non-GGUF endpoint wording.
- `scripts/validate_runtime_proof_action_queue.py` and hub readiness validation pass.

## Out Of Scope

- Running endpoint pilots.
- Resolving LM Studio model support.
- Downloading artifacts.
