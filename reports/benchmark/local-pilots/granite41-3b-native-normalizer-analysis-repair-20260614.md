# Granite 4.1 3B Native Normalizer Analysis Repair

Run ID: `ibm-granite-granite-4-1-3b-granite-native-normalizer-analysis-20260614-021344`
Created: `2026-06-13T16:13:53.172849+00:00`
Model: `ibm-granite/granite-4.1-3b`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, score-only `granite-native-tool-call` normalizer
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/ibm-granite-granite-4-1-3b-granite-native-normalizer-analysis-20260614-021344`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 1 |
| Pass rate | 0.333 |

## Failure Pattern

The normalizer analysis did not improve scoring over the raw strict run. Granite
still passed only the invalid-tool refusal and failed both exact tool-call cases.

## Decision

Do not promote `ibm-granite/granite-4.1-3b` from this analysis. Analysis-only
normalizer variants cannot promote by policy.
