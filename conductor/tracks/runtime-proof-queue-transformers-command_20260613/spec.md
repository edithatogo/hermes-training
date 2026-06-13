# Specification: Runtime Proof Queue Transformers Command

## Overview

The runtime proof queue had a concrete `hf-transformers` environment, but its
command template fell back to the generic coverage builder. That was not enough
for the top queue entries because it did not describe how to produce a new
bounded local proof.

## Goals

- Route `hf-transformers` Mac runtime proof entries to `scripts/run_transformers_pilot_benchmark.py`.
- Keep execution bounded to the BFCL-style pilot suite.
- Preserve strict Hermes scoring through `--require-no-extra-tool-text`.
- Keep SSD cache expectations visible in the generated command card.

## Acceptance Criteria

- `hf-transformers` `mac-runtime-proof` command templates use the bounded Transformers pilot.
- The command includes `--device auto`, `--dtype float16`, and `--require-no-extra-tool-text`.
- Unit coverage verifies the command shape.
- Regenerated queue reports show the updated command for the top Transformers candidate.
- Queue validation and hub readiness validation pass.

## Out Of Scope

- Downloading or running `hf-transformers` candidates.
- Changing candidate ranking.
- Promoting any model based on command-template changes alone.
