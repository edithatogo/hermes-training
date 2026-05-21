# License Review: Qwen3 Strict Tool-Call Expanded V1

## Scope

- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter candidate: `gemma4/experiments/qwen3-4b-strict-toolcall-expanded/lora_adapter`
- Dataset candidate: `gemma4/data/strict_tool_call/expanded_splits_v1`
- Review date: 2026-05-22

## Current Decision

GitHub source publication is acceptable for the small reproducibility artifacts already committed.

Hugging Face publication remains BLOCKED:

- Adapter publication is blocked by benchmark quality: held-out strict pass rate is `0.250`, below the required `1.000`.
- Dataset publication is blocked pending final redistribution review of the original mirrored seed source and accepted dataset scope.
- Merged weights and GGUF publication are blocked until upstream model license and redistribution terms are reviewed for the exact artifact type.

## Evidence Recorded

- Expanded examples are hand-authored synthetic records for local training.
- Dataset token audit exists at `dataset-token-audit.json`.
- Contamination guard reports zero overlap between `raw/expansion_seed_v1.jsonl` and the held-out suite.
- The materialized splits include original mirrored regression seed examples and therefore cannot be represented as fully held-out publication data.

## Required Before Hugging Face

- Confirm and cite the exact upstream license for `Qwen/Qwen3-4B-MLX-4bit`.
- Confirm whether the original mirrored seed examples can be redistributed in a public dataset repo.
- Decide whether to publish only `raw/expansion_seed_v1.jsonl` or the full materialized splits.
- Add final model and dataset cards with exact benchmark commands, raw artifact paths, and limitations.
