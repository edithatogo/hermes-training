# MLX Direct Loglikelihood Smoke: MiniCPM5 1B MLX

Run ID: `minicpm5-1b-mlx-loglikelihood-smoke-20260612`
Created: 2026-06-11T16:07:04.347582+00:00
Model: `openbmb/MiniCPM5-1B-MLX`
Suite: `benchmarks/lm_loglikelihood/smoke.jsonl`
Mode: `mlx-direct`
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood/minicpm5-1b-mlx-loglikelihood-smoke-20260612`
HF cache: `/Volumes/PortableSSD/huggingface/hub/models--openbmb--MiniCPM5-1B-MLX`

## Result

| Metric | Value |
|---|---:|
| Cases | 1 |
| Total continuation tokens | 1 |
| Mean avg logprob | -1.000000 |
| Greedy match rate | 1.000 |
| Load latency seconds | 62.387 |
| Score latency seconds | 0.600 |
| Snapshot size | 592M |

## Case

| Case | Continuation tokens | Loglikelihood | Avg logprob | Greedy match |
|---|---:|---:|---:|---|
| `capital-france` | 1 | -1.000000 | -1.000000 | `true` |

## Decision

This proves SSD-backed acquisition, MLX load, and direct prompt/continuation
scoring for `openbmb/MiniCPM5-1B-MLX` on the Mac lane. It is not a Hermes
adapter, tool-call benchmark, or publication-quality scorecard. Next gates are
Hermes utility prompts, extraction/tool-call smokes, and a role decision versus
Qwen3.5 0.8B/2B.
