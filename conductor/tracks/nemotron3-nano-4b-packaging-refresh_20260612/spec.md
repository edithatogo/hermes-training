# Specification: Nemotron 3 Nano 4B Packaging Refresh

## Overview

Nemotron 3 Nano 4B now has an official BF16 base and current local packaging
lanes that are relevant for Hermes helper/runtime work on Mac and Colab.

This refresh focuses on:

- `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16`
- `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`
- `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF`
- `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit`

## Scope

- Verify the official base repository and current local packaging pages.
- Update the machine-readable model radar and the human-facing shortlist.
- Add a concise scan report describing the local packaging lanes.

## Out Of Scope

- No training runs.
- No runtime proof claims.
- No benchmark claims.

## Acceptance Criteria

- The radar includes the official 4B Nemotron base and local packaging lanes.
- The docs keep the family in runtime/helper lanes.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the family now has an official base and Mac-usable packaging.
- Remaining gap: runtime proof for the local packaging variants.
