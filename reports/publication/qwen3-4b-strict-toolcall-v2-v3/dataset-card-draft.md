# Dataset Card Draft: Qwen3 4B Strict Tool-Call V2/V3

## Dataset

- V2: `gemma4/data/strict_tool_call/expanded_splits_v2`
- V3: `gemma4/data/strict_tool_call/expanded_splits_v3_no_think`

These datasets extend the strict tool-call lane with non-heldout synthetic examples. V2 adds explicit format guards for the Qwen empty-thinking-wrapper failure mode. V3 duplicates V2 training rows with `/no_think` prefixed to the first user turn while leaving validation and test splits unchanged.

## Split Summary

| Dataset | Split | Rows | Tokens |
|---|---|---:|---:|
| V2 | train | 40 | 10,268 |
| V2 | val/valid | 5 | 1,337 |
| V2 | test | 5 | 1,314 |
| V3 | train | 80 | 20,655 |
| V3 | val/valid | 5 | 1,337 |
| V3 | test | 5 | 1,314 |

Token audits:

- `reports/publication/qwen3-4b-strict-toolcall-v2-dataset-token-audit.json`
- `reports/publication/qwen3-4b-strict-toolcall-v3-dataset-token-audit.json`

## Contamination Policy

Held-out benchmark examples must not be copied, paraphrased, or mechanically transformed into training data. V2 raw data and V3 splits were audited for held-out overlap before training. The mirrored suite overlap remains documented as regression-only data and cannot support publication claims.
