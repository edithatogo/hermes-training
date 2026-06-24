# Qwen3 v9 Runtime Safety/Refusal Profile Selection - 2026-06-24

## Decision

Select `qwen3-v9-no-think-prefill-refusal-marker-normalized` for Hermes
runtime safety/refusal integration evidence.

This is a runtime-profile selection, not a raw model-weight claim. The selected
path uses:

- user prefix: `/no_think`
- assistant prefill: `<think>\n\n</think>\n\n`
- normalizers:
  - `strip-leading-empty-think-prefix`
  - `text-refusal-forbidden-marker-redaction-v1`

The refusal-marker normalizer is constrained to text-mode refusals that contain
no `tool_call` tags. It must not rewrite valid tool-call JSON.

## Evidence

| Candidate | Strict pass | JSON valid | Argument accuracy | Empty think cases | Residual failures | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| raw v9 full140 with runtime profile | 0.875 | 1.000 | 1.000 | 0 | 1 | Not publishable as raw weights |
| v9 runtime-normalized profile | 1.000 | 1.000 | 1.000 | 0 | 0 | Selected for Hermes runtime evidence |
| raw v10 customer-delete repair | 0.750 | 1.000 | 0.667 | 0 | 2 | Rejected |

Run roots:

- Raw v9: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v9-full140-runtime-profile-prefill-only-20260624`
- Runtime-normalized v9: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v9-runtime-profile-refusal-marker-normalized-20260624`
- Raw v10: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v10-customer-delete-refusal-marker-repair-20260624`

Primary reports:

- `reports/benchmark/official-candidates/qwen3-v9-runtime-profile-refusal-marker-repair-run-20260624.md`
- `reports/benchmark/official-candidates/qwen3-v9-runtime-refusal-marker-normalization-proof-20260624.md`
- `reports/benchmark/official-candidates/qwen3-v10-customer-delete-refusal-marker-repair-run-20260624.md`

## Claim Boundary

Hermes can use the selected v9 runtime profile as a safety/refusal integration
path for the pinned suite. Do not publish v9 or v10 weights from this evidence.
The raw model-weight claim remains blocked until an unnormalized run reaches the
same gate:

- strict pass `1.000`
- JSON validity `1.000`
- argument accuracy `1.000`
- empty-think prefix cases `0`
- residual strict failures `0`

## Next Raw-Weight Work

If raw weight publication becomes necessary, use the v9 normalized diff as the
target for a new isolated refusal repair. Avoid broader v10-style SFT until the
single marker echo can be removed without regressing argument copying.
