# Qwen3.5 0.8B Strict-Suffix Copy-Exact Repair

Run ID: `qwen-qwen3-5-0-8b-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)`
Created: `2026-06-13T15:48:50.051505+00:00`
Model: `Qwen/Qwen3.5-0.8B`
Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
Variant: `strict-suffix-copy-exact`
Mode: local MLX generation, SSD cache, strict no-extra-tool-text scoring
Output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen-qwen3-5-0-8b-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)`

## Command Boundary

The run was launched through the prompt/profile repair selector with
`--execute --confirm-local-run`. The generated run id preserved a literal
`$(date +%Y%m%d-%H%M%S)` expression because the old command template shell-quoted
the run id. The experiment templates now use `RUN_STAMP=$(date +%Y%m%d-%H%M%S)`
and `${RUN_STAMP}` instead.

## Result

| Metric | Value |
|---|---:|
| Cases | 3 |
| Passed | 0 |
| Pass rate | 0.000 |

## Failure Pattern

The strict suffix did not repair Hermes tool-call behavior. The model emitted
long `Thinking Process` prose on all three cases. No valid Hermes tool calls
were extracted for the two tool-call cases. The invalid-tool case had the right
refusal direction, but repeated excluded unavailable-tool text, so it failed the
strict excludes/no-extra-text gate.

## Decision

Do not promote `Qwen/Qwen3.5-0.8B` from this repair. Keep it as helper or
prompt-repair research evidence only. The next Qwen3.5 0.8B repair attempt
should use `qwen-no-think-prefill` or `empty-output-retry`, not another
strict-suffix-only run.
