# Qwen3 v12 BFCL parallel repair 30-case smoke

Run ID: `qwen3-v12-bfcl-parallel-repair-30-20260626`

Status: `completed-no-promotion-parallel-single-call-collapse`

The v12 adapter was trained from the v11 selected-slice repair baseline with 10 additional BFCL selected parallel repair rows. The dataset intentionally targeted only the residual parallel-call failure after the handler bridge fixed blank/prose scored outputs.

## Training

- Config: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v12-bfcl-parallel-repair.yaml`
- Dataset: `gemma4/data/strict_tool_call/expanded_splits_v12_bfcl_parallel_repair`
- Repair rows: 10
- Iterations: 80
- Final train loss: `0.947`
- Final validation loss: `0.993`
- Peak memory: `3.770 GB`

## BFCL selected smoke

- Selected `simple_python`: `100.00%`
- Selected `multiple`: `100.00%`
- Selected `parallel`: `0.00%`
- Selected non-live overall: `33.33%`
- BFCL overall CSV value from this partial smoke: `3.33%`

## Row audit

The v12 run preserved the v11 handler-bridge output shape: all 30 selected rows contain visible `<tool_call>` blocks. The residual blocker is parallel single-call collapse:

- `simple_python`: 10/10 visible tool calls
- `multiple`: 10/10 visible tool calls
- `parallel`: 10/10 visible tool calls, 10/10 single tool blocks, 0/10 multi-tool blocks

BFCL reports `Wrong number of functions.` for the selected parallel failures.

## Boundary

This is private fail-closed runtime repair evidence only. It is not a BFCL leaderboard score, not a passing Hermes tool-call claim, and not a model publication gate pass. Treat v12 as `completed-no-promotion`. The next repair should test runtime continuation or a stronger parallel-only curriculum because the model still emits exactly one call for every selected parallel prompt.
