# Specification: Qwen3 Publication Evidence And Runtime Normalization

## Overview

Close the immediate evidence gaps after the expanded strict tool-call retrain without weakening the held-out benchmark gate. This track records dataset token evidence, license review, and the runtime-only empty-think normalization contract for Hermes integration.

## Requirements

- Record standalone dataset token counts for `gemma4/data/strict_tool_call/expanded_splits_v1`.
- Keep token-audit output small and source-control safe.
- Record a license and redistribution review for the expanded strict tool-call dataset and adapter candidate.
- Keep Hugging Face publication blocked if either quality or redistribution scope is insufficient.
- Document empty leading `<think></think>` normalization as a runtime integration helper only.
- Preserve strict held-out pass rate `1.000` as the only adapter publication gate.

## Acceptance Criteria

- `scripts/dataset_token_audit.py` can write a JSON report.
- `reports/publication/qwen3-4b-strict-toolcall-expanded/dataset-token-audit.json` exists.
- `reports/publication/qwen3-4b-strict-toolcall-expanded/dataset-card-draft.md` exists.
- `reports/publication/qwen3-4b-strict-toolcall-expanded/license-review.md` exists.
- The publication run card and checklist reference the token audit and license review.
- Runtime normalization is documented under `reports/runtime/qwen3-runtime-normalization/`.
- Normalization self-tests pass.

## Out Of Scope

- Publishing to Hugging Face.
- Changing strict benchmark scoring.
- Downloading new model weights.
- Moving large artifacts into Git.
