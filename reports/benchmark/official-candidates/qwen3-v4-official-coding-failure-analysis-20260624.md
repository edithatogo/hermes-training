# Qwen3 v4 Official Coding Failure Analysis - 2026-06-24

Candidate: `qwen3-4b-strict-toolcall-v4-targeted`

Source result:
`reports/benchmark/official-candidates/qwen3-v4-official-coding-evalplus-rerun-20260624.json`

## Score Baseline

| Metric | Value |
| --- | ---: |
| HumanEval base pass@1 | 0.518 |
| HumanEval+ pass@1 | 0.482 printed / 0.488 JSON |
| Tasks | 164 |
| Base pass count | 85 |
| Plus pass count | 80 |

## Failure Shape

| Bucket | Count | Notes |
| --- | ---: | --- |
| Pass both base and plus | 79 | Fully passing tasks. |
| Base fail | 79 | Not coding-ready; most misses are not EvalPlus-only edge cases. |
| Plus-only fail | 6 | Cleanest target for edge-case repair. |
| Empty completion | 23 | Generation/protocol failure. |
| Syntax or pre-test failure | 13 | Full solution fails before concrete failed tests are recorded. |
| Likely truncated/runaway | 12 | Completion boundary or token-budget problem. |
| Missing return | 14 | Plausible code body but no returned value. |
| Debug/example leakage | 5 | Generated examples or debug prints leak into body. |

## Decision

Targeted coding repair is worthwhile, but do not start with broad fine-tuning.

The first repair should be a coding-generation repair experiment:

- stricter completion stop rules
- non-empty body validation
- no examples/debug text in generated completions
- larger token budget only where truncation is detected
- failed-only regeneration and re-score

Only after that should we create a narrow SFT repair dataset. The cleanest
fine-tuning candidates are the 6 plus-only EvalPlus failures:

- `HumanEval/22`
- `HumanEval/25`
- `HumanEval/46`
- `HumanEval/55`
- `HumanEval/76`
- `HumanEval/97`

## Claim Boundary

This is diagnostic evidence only. The current scored coding result remains
HumanEval pass@1 `0.518` and HumanEval+ pass@1 `0.482` printed / `0.488` JSON.
Do not make a broad coding claim from this candidate.
