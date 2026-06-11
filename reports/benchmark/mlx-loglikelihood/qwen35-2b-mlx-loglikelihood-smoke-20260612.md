# MLX Direct Loglikelihood Smoke: Qwen3.5 2B

Run ID: `qwen35-2b-mlx-loglikelihood-smoke-20260612`
Created: 2026-06-11T15:14:00.778348+00:00
Model: `Qwen/Qwen3.5-2B`
Suite: `benchmarks/lm_loglikelihood/smoke.jsonl`
Mode: `mlx-direct`
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood/qwen35-2b-mlx-loglikelihood-smoke-20260612`
HF cache: `/Volumes/PortableSSD/huggingface/hub/models--Qwen--Qwen3.5-2B`

## Result

| Metric | Value |
|---|---:|
| Cases | 1 |
| Total continuation tokens | 1 |
| Mean avg logprob | -0.750000 |
| Greedy match rate | 1.000 |
| Load latency seconds | 447.977 |
| Score latency seconds | 0.769 |
| Snapshot size | 4.3G |

## Case

| Case | Continuation tokens | Loglikelihood | Avg logprob | Greedy match |
|---|---:|---:|---:|---|
| `capital-france` | 1 | -0.750000 | -0.750000 | `true` |

## Decision

This proves acquisition, MLX load, and direct prompt/continuation scoring for
`Qwen/Qwen3.5-2B` on the SSD-backed Mac lane. It is not a Hermes adapter, full
candidate benchmark, or publication-quality scorecard.

