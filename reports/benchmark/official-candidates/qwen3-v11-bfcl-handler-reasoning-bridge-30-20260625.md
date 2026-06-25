# Qwen3 v11 BFCL handler reasoning bridge 30-case smoke

Run ID: `qwen3-v11-bfcl-handler-reasoning-bridge-30-20260625`

Status: `handler-bridge-output-shape-fixed-parallel-still-blocked`

This run moved below the normalizing proxy and applied the guarded local BFCL handler patch in `scripts/patch_bfcl_qwen_reasoning_bridge.py`. The patch promotes complete reasoning-side `<tool_call>` blocks into BFCL's scored `result` field only when the visible completion has no tool-call block.

## Result

- Selected `simple_python`: `100.00%`
- Selected `multiple`: `100.00%`
- Selected `parallel`: `0.00%`
- Selected non-live overall: `33.33%`
- BFCL overall CSV value from this partial smoke: `3.33%`

## Row shape

All 30 selected rows now contain visible `<tool_call>` blocks in the scored `result` field:

- `simple_python`: 10/10 visible tool calls, 0 blank, 0 prose-only
- `multiple`: 10/10 visible tool calls, 0 blank, 0 prose-only
- `parallel`: 10/10 visible tool calls, 0 blank, 0 prose-only

## Boundary

This is private fail-closed runtime repair evidence only. It is not a BFCL leaderboard score, not a passing Hermes tool-call claim, and not a model publication gate pass. The next concrete blocker is parallel semantics: build a narrow v12 parallel-call repair dataset and runtime smoke because the selected parallel cases still score `0.00%`.
