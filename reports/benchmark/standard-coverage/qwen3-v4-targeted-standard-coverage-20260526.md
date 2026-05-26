# Standard Benchmark Coverage: qwen3-4b-strict-toolcall-v4-targeted

Run ID: `qwen3-v4-targeted-standard-coverage-20260526`
Status: `pilot-only`
Local adapter gate ready: `true`
Public release blocked: `true`

## Coverage

| Suite | Tier | Status | Metric | Evidence | Required for |
|---|---|---|---|---|---|
| `local-heldout-strict-tool-call` | candidate-local | `passed` | strict held-out pass 1.000 | reports/benchmark/publication-readiness-gate-20260524.md | local adapter publication claim |
| `local-bfcl-style-pilot` | pilot | `present` | BFCL-style pilot 0.667 | reports/benchmark/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-pilots-20260525.md | pilot-only model card positioning |
| `local-ifeval-style-pilot` | pilot | `present` | IFEval-style pilot 0.667 | reports/benchmark/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-pilots-20260525.md | pilot-only model card positioning |
| `local-coding-sanity-pilot` | pilot | `present` | coding sanity pilot 1.000 | reports/benchmark/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-pilots-20260525.md | pilot-only model card positioning |
| `official-ifeval-pilot` | official-pilot | `present` | prompt strict 0.760 | reports/benchmark/official-ifeval/qwen3-4b-v4-targeted-ifeval-pilot-20260526.md | official harness readiness |
| `publication-bundle` | release-gate | `blocked` | local quality gates checked; public release gates remain blocked | reports/publication/qwen3-4b-strict-toolcall-v4-targeted/publish-readiness-checklist.md | public Hugging Face release |
| `official-bfcl` | official-candidate | `missing` |  | none | broad tool-calling benchmark claim |
| `lm-eval-selected-smoke` | official-pilot | `present` | limit 10 selected MLX direct smoke scored | reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit10-20260526.md | official harness readiness |
| `lm-eval-selected` | official-candidate | `missing` |  | reports/benchmark/lm-eval/qwen3-4b-v4-targeted-lm-eval-selected-smoke-20260526.md | general benchmark claim |
| `official-coding` | official-candidate | `missing` |  | none | coding benchmark claim |
| `safety-refusal` | official-candidate | `missing` |  | none | safety/refusal claim |
| `ruler-long-context` | official-candidate | `missing` |  | none | long-context claim |

## Decision

The adapter can be described as local strict Hermes-agent evidence with pilot-only benchmark support.
Do not describe it as broadly benchmarked until the missing official candidate suites are run or explicitly excluded.
