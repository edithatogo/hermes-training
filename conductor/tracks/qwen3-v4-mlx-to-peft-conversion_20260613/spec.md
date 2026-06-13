# Specification: Qwen3 V4 MLX To PEFT Conversion

## Overview

Produce a PEFT-shaped adapter package from the existing Qwen3 v4 MLX LoRA weights so future Colab/Azure work can test whether the converted artifact loads under Transformers/PEFT.

## Acceptance Criteria

- Add a converter that maps MLX LoRA keys to PEFT LoRA key names and transposes matrix orientation.
- Write converted adapter artifacts only to `/Volumes/PortableSSD`.
- Record a lightweight conversion report under `reports/cloud/`.
- Label the artifact experimental until a PEFT load and behavior smoke passes.
