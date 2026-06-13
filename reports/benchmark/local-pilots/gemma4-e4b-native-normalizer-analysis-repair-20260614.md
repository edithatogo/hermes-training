# Gemma E4B Native Normalizer Analysis Repair

Run ID: `mlx-community-gemma-4-e4b-it-qat-4bit-gemma-native-normalizer-analysis-20260614-021019`
Created: `2026-06-13T16:10:39.448616+00:00`
Model: `mlx-community/gemma-4-E4B-it-qat-4bit`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, score-only `gemma-native-tool-call` normalizer
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/mlx-community-gemma-4-e4b-it-qat-4bit-gemma-native-normalizer-analysis-20260614-021019`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The analysis-only normalizer did not change the score. Outputs still contained
Gemma thought-channel text and payloads that lacked exact Hermes `name` and
`arguments` fields. The invalid-tool case also failed the strict excludes gate.

## Decision

Do not promote `mlx-community/gemma-4-E4B-it-qat-4bit` from this analysis. The
normalizer did not produce promotion-grade strict evidence, and analysis-only
variants cannot promote by policy.
