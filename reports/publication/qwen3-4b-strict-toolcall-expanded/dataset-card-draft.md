# Dataset Card Draft: Qwen3 Strict Tool-Call Expanded V1

## Identity

- Dataset path: `gemma4/data/strict_tool_call/expanded_splits_v1`
- Source files: `gemma4/data/strict_tool_call/raw/seed.jsonl`, `gemma4/data/strict_tool_call/raw/expansion_seed_v1.jsonl`
- Intended use: local supervised fine-tuning for Hermes-style strict tool-call formatting.
- Publication status: BLOCKED for Hugging Face dataset publication.

## Composition

| Split | Rows | Tokens | P50 | P95 | Max |
|---|---:|---:|---:|---:|---:|
| train | 33 | 9,081 | 249 | 437 | 752 |
| val | 4 | 1,026 | 244 | 255 | 288 |
| valid | 4 | 1,026 | 244 | 255 | 288 |
| test | 5 | 1,314 | 247 | 264 | 311 |

Token counts were produced with `Qwen/Qwen3-4B-MLX-4bit` using:

```bash
source scripts/env.sh
HF_HUB_OFFLINE=1 ./.venv/bin/python scripts/dataset_token_audit.py \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --data gemma4/data/strict_tool_call/expanded_splits_v1 \
  --splits train val valid test \
  --output reports/publication/qwen3-4b-strict-toolcall-expanded/dataset-token-audit.json
```

## Coverage

- Behavior buckets: `json_validity`, `argument_correctness`, `invalid_tool_handling`, `multi_turn_repair`
- Raw expansion count: 32 hand-authored synthetic examples, 8 examples per bucket.
- Materialized split count: 42 unique examples plus `valid.jsonl` as the MLX-compatible alias of `val.jsonl`.

## Contamination Status

`raw/expansion_seed_v1.jsonl` audited with zero overlap against both local benchmark suites:

- `benchmarks/tool_call_local/suite.json`
- `benchmarks/tool_call_local/heldout_suite.json`

The materialized splits intentionally include the original 10-example seed aligned with the mirrored regression suite. That mirrored seed is not held-out publication evidence.

## License And Redistribution

The expansion examples are hand-authored synthetic examples created for this repository. They can remain in GitHub for reproducibility.

Hugging Face dataset publication is still blocked until:

- the original mirrored seed source and redistribution scope are explicitly reviewed
- the dataset publication scope is accepted
- a final dataset card is approved

## Known Limitations

- The dataset is too small to establish publishable tool-call generalization.
- It did not produce a publishable adapter: held-out strict pass rate remained `0.250`.
- It does not solve Qwen empty leading `<think></think>` wrapper behavior by itself.
