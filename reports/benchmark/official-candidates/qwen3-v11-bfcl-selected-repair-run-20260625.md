# Qwen3 v11 BFCL Selected Repair Run

Run ID: `qwen3-v11-bfcl-text-prefix-bridge-30-20260625`
Status: `trained-but-bfcl-bridge-regressed`
Candidate: `qwen3-4b-strict-toolcall-v11-bfcl-selected-repair`

Private fail-closed evidence only. This is not a BFCL leaderboard score, not a
passing Hermes tool-call claim, and not a model publication gate pass.

## Training

| Metric | Value |
|---|---:|
| Train rows | `820` |
| Valid rows | `5` |
| Iterations | `180` |
| Final train loss | `0.596` |
| Final val loss | `0.791` |
| Trained tokens | `53898` |
| Peak memory | `3.794 GB` |
| Duration | `475.1s` |

Adapter:
`gemma4/experiments/qwen3-4b-strict-toolcall-v11-bfcl-selected-repair/lora_adapter`

## BFCL 30-Case Bridge Smoke

| Metric | v10 bridge baseline | v11 repair |
|---|---:|---:|
| Overall Acc | `0.0033` | `0.0008` |
| Non-Live Overall Acc | `0.0333` | `0.0083` |
| simple_python AST | `0.100` | `0.100` |
| multiple AST | `0.100` | `0.000` |
| parallel AST | `0.000` | `0.000` |

## Row Audit

| Category | Rows | Blank result | Visible tool | Reasoning tool | Prose no tool | Decoded empty |
|---|---:|---:|---:|---:|---:|---:|
| `simple_python` | `10` | `1` | `1` | `9` | `8` | `9` |
| `multiple` | `10` | `3` | `0` | `10` | `7` | `10` |
| `parallel` | `10` | `1` | `3` | `7` | `6` | `7` |

Parallel also had `3` rows with one visible decoded call that still failed the
wrong-count checker.

## Decision

The adapter trained successfully, but it did not repair BFCL's scored
visible-content channel. The bounded bridge smoke regressed versus the previous
30-case bridge evidence: `multiple` dropped from `10%` to `0%`, and `parallel`
remained `0%`.

Do not expand v11 to the full selected BFCL slice. The next blocker is not
dataset materialization or local training capacity; it is runtime/content-channel
alignment. Prioritize one of these before more SFT:

- extract or map complete `reasoning_content` tool calls into BFCL-scored text
  for completions, not only chat completions
- adjust the MLX/BFCL generation template so tool calls land in scored
  `result` text
- rerun only the 30-case smoke after that runtime fix

