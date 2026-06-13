# Specification: Qwen3 V4 Colab Full Scorecard Portability

## Overview

Determine whether the current public Qwen3 v4 strict Hermes tool-call adapter can be run on Colab for the no-limit selected-task `lm-eval` scorecard.

## Goals

- Probe Colab GPU runtime availability through `google-colab-cli`.
- Confirm the public Hugging Face adapter repo is visible from Colab.
- Test whether `mlx` and `mlx_lm` can be installed/imported on the Colab runtime.
- Record a scorecard route decision before launching any expensive benchmark.

## Acceptance Criteria

- A tracked Colab report records either a viable Colab MLX route or a concrete portability blocker.
- The report does not claim benchmark scores.
- If blocked, the next route is explicit: publish/produce a PEFT or fused artifact, or keep the full scorecard on a Mac/MLX runner.

## Out Of Scope

- Running the full selected-task benchmark.
- Uploading new model artifacts.
- Changing Hugging Face model visibility.
