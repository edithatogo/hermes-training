# Nemotron 3 Nano 4B OptiQ Strict-Suffix Prompt Repair

Run ID: `mlx-community-nvidia-nemotron-3-nano-4b-optiq-4bit-strict-suffix-copy-exact-20260614-021844`
Created: `2026-06-13T16:19:05.181460+00:00`
Model: `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, strict suffix plus exact-copy instruction
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/mlx-community-nvidia-nemotron-3-nano-4b-optiq-4bit-strict-suffix-copy-exact-20260614-021844`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The model emitted reasoning text before incomplete or missing tool-call tags.
The invalid-tool case produced the target refusal but included thought text and
many repeated `<|im_end|>` tokens, failing strict no-extra-text scoring.

## Decision

Do not promote `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` from this
repair. A future revisit should use grammar/envelope-constrained output rather
than prompt suffix alone.
