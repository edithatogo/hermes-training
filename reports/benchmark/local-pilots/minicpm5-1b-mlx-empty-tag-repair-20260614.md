# MiniCPM5 1B MLX Empty-Tag Prompt Repair

Run ID: `openbmb-minicpm5-1b-mlx-minicpm-empty-tag-repair-20260614-020121`
Created: `2026-06-13T16:01:30.198902+00:00`
Model: `openbmb/MiniCPM5-1B-MLX`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Mode: local MLX generation, SSD cache, concise `<tool_call>` envelope suffix
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/openbmb-minicpm5-1b-mlx-minicpm-empty-tag-repair-20260614-020121`

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The concise tag instruction still produced reasoning text and malformed or
schema-like tool fragments. The invalid-tool case failed by describing and
mentioning the unavailable delete function before the refusal.

## Decision

Do not promote `openbmb/MiniCPM5-1B-MLX` from prompt-only repair. All three
queued local MiniCPM prompt variants scored `0/3`; the next useful work is a
grammar/envelope-constrained path or moving to the next local candidate.
