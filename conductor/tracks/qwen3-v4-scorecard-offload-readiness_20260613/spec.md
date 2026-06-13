# Specification: Qwen3 V4 Scorecard Offload Readiness

## Overview

After the local no-limit MLX scorecard proved impractical, determine whether the exact Qwen3 v4 adapter can be moved to Colab or Azure for the same benchmark.

## Acceptance Criteria

- Add a validator that inspects the scorecard plan and adapter metadata.
- Fail closed when the adapter is MLX-native and not directly loadable through CUDA Transformers/PEFT.
- Produce a report under `reports/cloud/` with the next action.
- Keep broad benchmark claims blocked unless exact-adapter portability is proven.
