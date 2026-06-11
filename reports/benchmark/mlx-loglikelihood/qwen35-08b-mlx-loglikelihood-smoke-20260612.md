# MLX Direct Loglikelihood Smoke: Qwen3.5 0.8B

Run ID: `qwen35-08b-mlx-loglikelihood-smoke-20260612`
Created: 2026-06-11T15:02:29.083744+00:00
Model: `Qwen/Qwen3.5-0.8B`
Suite: `benchmarks/lm_loglikelihood/smoke.jsonl`
Mode: `mlx-direct`
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood/qwen35-08b-mlx-loglikelihood-smoke-20260612`
HF cache: `/Volumes/PortableSSD/huggingface/hub/models--Qwen--Qwen3.5-0.8B`

## Result

| Metric | Value |
|---|---:|
| Cases | 1 |
| Total continuation tokens | 1 |
| Mean avg logprob | -2.062500 |
| Greedy match rate | 1.000 |
| Load latency seconds | 224.249 |
| Score latency seconds | 1.037 |
| Snapshot size | 1.7G |

## Case

| Case | Continuation tokens | Loglikelihood | Avg logprob | Greedy match |
|---|---:|---:|---:|---|
| `capital-france` | 1 | -2.062500 | -2.062500 | `true` |

## Decision

This proves acquisition, MLX load, and direct prompt/continuation scoring for
`Qwen/Qwen3.5-0.8B` on the SSD-backed Mac lane. It is not a Hermes adapter, full
candidate benchmark, or publication-quality scorecard.

