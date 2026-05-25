# Release Decision: Qwen3 4B Strict Tool-Call V4 Targeted

Date: 2026-05-25

## Decision

GitHub evidence publication: **approved and versioned**.

Hugging Face adapter publication: **approved as public experimental release**.

Private Hugging Face draft adapter: **superseded by public release**.

Dataset publication: **blocked**.

Merged weights or GGUF publication: **out of scope and blocked**.

## Public Release Positioning

The local strict quality gate is satisfied. Public release is approved with
narrow, explicit positioning:

- This is an experimental strict Hermes tool-call LoRA adapter.
- It requires `/no_think` plus assistant prefill `<think>\n\n</think>\n\n`.
- Repo-native pilot scores are disclosed as pilot-only engineering evidence.
- It is not presented as an official BFCL, IFEval, HumanEval, MBPP, or broad
  production tool-use benchmark winner.

Human approval was recorded on 2026-05-25 by the user instruction:
`Address all of the issues and make it public`.

## Evidence Approved For GitHub

- Run card: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/run-card.md`
- Publish checklist: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/publish-readiness-checklist.md`
- License review: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/license-review.md`
- Model card draft: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/hf-model-card-draft.md`
- Dataset overlap audit: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-overlap-audit.json`
- Dataset token audit: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-token-audit.json`
- Dataset source audit: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-source-audit.json`
- Redistribution review: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/redistribution-review.md`
- Dataset publication scope: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-publication-scope.md`
- Dataset card draft: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/hf-dataset-card-draft.md`
- Pilot failure analysis: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/pilot-failure-analysis-20260526.md`
- Local pilot report: `reports/benchmark/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-pilots-20260525.md`

## Quality Evidence

Required runtime condition:

```text
user_prefix=/no_think
assistant_prefill=<think>\n\n</think>\n\n
```

Strict held-out local tool-call gate:

- Suite: `benchmarks/tool_call_local/heldout_suite.json`
- Strict pass: `1.000`
- JSON validity: `1.000`
- Argument correctness: `1.000`
- Invalid-tool handling: `1.000`
- Multi-turn repair: `1.000`
- Raw output: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v4-targeted-heldout-prefill-20260525`

Mirrored regression:

- Suite: `benchmarks/tool_call_local/suite.json`
- Strict pass: `1.000`
- Raw output: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-v4-targeted-mirrored-prefill-20260525`

Local pilot benchmarks:

| Pilot | Pass rate | Scope |
|---|---:|---|
| BFCL-style pilot | `0.667` | repo-native pilot only |
| IFEval-style pilot | `0.667` | repo-native pilot only |
| Coding sanity pilot | `1.000` | repo-native pilot only |

These pilot scores are useful engineering evidence, not official benchmark
claims.

## Hugging Face Release Evidence

Adapter repo:

```text
https://huggingface.co/edithatogo/qwen3-4b-hermes-lora
```

Verification:

```text
local adapters.safetensors sha256: 42e4364d2b8fe8d467295a4581d983623a296ec31aff006c514c6ca2d113039e
HF downloaded adapters.safetensors sha256: 42e4364d2b8fe8d467295a4581d983623a296ec31aff006c514c6ca2d113039e
HF adapter-weight revision verified during private draft stage: bec399b04be9ba7ba67d3a58926367bf2cb930e7
```

This verifies artifact preservation. The same artifact is approved for public
release with the limitations in the final model card.

## Machine Gate

Public release gate:

```bash
./.venv/bin/python scripts/validate_publication_bundle.py \
  reports/publication/qwen3-4b-strict-toolcall-v4-targeted \
  --require-ready
```

The public release gate must pass before or at the same commit that changes the
Hugging Face repository visibility.

## Next Actions

1. Keep the current public model card scoped to strict Hermes local tool-call
   behavior and pilot-only benchmark evidence.
2. Run broader official suites later before making stronger benchmark claims.
3. Continue iterating on BFCL-style and IFEval-style pilot failures in the next
   adapter track.
4. Publish a cleaned synthetic-only dataset only after explicit human approval
   of `dataset-publication-scope.md`.
5. For any v6 experiment, start from V4 and require held-out strict pass to stay
   at `1.000` before considering pilot improvements.
