# MLX Direct Loglikelihood Smoke

Date: 2026-05-26

## Scope

Add a repo-native prompt/continuation loglikelihood harness for MLX causal LM
logits. This is the next valid path after `lm_eval --model local-completions`
reached the `mlx_lm.server` endpoint but failed because the server returns
generated-token `logprobs.content`, not legacy echoed prompt
`token_logprobs`.

This smoke is deliberately a no-download schema proof. It does not claim an
official `lm-eval` score.

Two scripts now exist:

- `scripts/run_mlx_loglikelihood_smoke.py` scores explicit JSONL
  prompt/continuation cases and has a mock mode for no-download schema checks.
- `scripts/run_mlx_lm_eval.py` is a direct `lm_eval` adapter scaffold for
  loglikelihood-only tasks; its self-test and dry-run pass, but it still needs a
  bounded non-mock task run before any score is reported.

## Commands

```bash
./.venv/bin/python scripts/run_mlx_loglikelihood_smoke.py \
  --mock-uniform \
  --run-id mlx-loglikelihood-mock-smoke-20260526 \
  --output-root /Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood

./.venv/bin/python scripts/run_mlx_lm_eval.py --self-test
./.venv/bin/python scripts/run_mlx_lm_eval.py --dry-run --run-id dry-test
```

## Result

| Metric | Value |
|---|---:|
| Cases | 2 |
| Continuation tokens | 2 |
| Mean avg logprob | -10.373491 |
| Greedy match rate | 0.000 |

Artifacts:

- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood/mlx-loglikelihood-mock-smoke-20260526/summary.json`
- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood/mlx-loglikelihood-mock-smoke-20260526/results.jsonl`
- `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood/mlx-loglikelihood-mock-smoke-20260526/summary.md`

## Decision

The direct scorer, adapter scaffold, and output schema are ready for a bounded
non-mock MLX run. The next step is to run the Qwen3 v4 adapter directly through
MLX logits on a tiny selected task limit. Keep `lm-eval-selected` blocked until
that non-mock path produces real scores.
