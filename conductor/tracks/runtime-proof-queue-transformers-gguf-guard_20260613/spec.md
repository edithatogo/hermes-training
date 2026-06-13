# Specification: Runtime Proof Queue Transformers GGUF Guard

## Overview

Some `hf-transformers` candidates describe their first runtime as
`Transformers or GGUF smoke`. The queue command generator previously tested for
`GGUF` text before checking the explicit environment, which caused those
Transformers candidates to receive endpoint/GGUF command templates.

## Goals

- Make explicit candidate environment win over free-text runtime notes.
- Keep `hf-transformers` candidates on the bounded Transformers pilot path.
- Keep GGUF endpoint pilots for actual GGUF/LM Studio/Ollama candidates.
- Regenerate the runtime proof queue after the bugfix.

## Acceptance Criteria

- `DJLougen/Harmonic-9B` and `Qwen/Qwen3.5-9B` receive `run_transformers_pilot_benchmark.py` command cards.
- A regression test prevents `hf-transformers` candidates from being routed to `run_endpoint_pilot_benchmark.py` merely because `first_runtime` mentions GGUF.
- Queue validation and hub readiness validation pass.

## Out Of Scope

- Running the affected pilots.
- Downloading model artifacts.
- Changing candidate ordering or promotion status.
