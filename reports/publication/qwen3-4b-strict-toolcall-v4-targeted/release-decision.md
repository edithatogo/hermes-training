# Release Decision: Qwen3 4B Strict Tool-Call V4 Targeted

Date: 2026-05-25

## Decision

GitHub evidence publication: **approved and versioned**.

Private Hugging Face draft adapter: **approved as private draft evidence**.

Public Hugging Face adapter publication: **blocked**.

Dataset publication: **blocked**.

Merged weights or GGUF publication: **out of scope and blocked**.

## Why This Is Not Public Yet

The local strict quality gate is satisfied, but public release requires more
than quality. The remaining public-release gates are:

- final standard benchmark positioning with pilot scores labeled correctly
- finalized Hugging Face model card
- explicit human publication approval

The release must stay fail-closed until those gates are checked in the
publish-readiness checklist.

## Evidence Approved For GitHub

- Run card: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/run-card.md`
- Publish checklist: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/publish-readiness-checklist.md`
- License review: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/license-review.md`
- Model card draft: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/hf-model-card-draft.md`
- Dataset overlap audit: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-overlap-audit.json`
- Dataset token audit: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-token-audit.json`
- Dataset source audit: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-source-audit.json`
- Redistribution review: `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/redistribution-review.md`
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

## Private Hugging Face Draft Evidence

Private draft repo:

```text
https://huggingface.co/edithatogo/qwen3-4b-hermes-lora
```

Verification:

```text
local adapters.safetensors sha256: 42e4364d2b8fe8d467295a4581d983623a296ec31aff006c514c6ca2d113039e
HF downloaded adapters.safetensors sha256: 42e4364d2b8fe8d467295a4581d983623a296ec31aff006c514c6ca2d113039e
HF main revision: bec399b04be9ba7ba67d3a58926367bf2cb930e7
```

This verifies artifact preservation only. It is not public release approval.

## Machine Gate

Current expected gate:

```bash
./.venv/bin/python scripts/validate_publication_bundle.py \
  reports/publication/qwen3-4b-strict-toolcall-v4-targeted \
  --expect-blocked
```

Future public release gate:

```bash
./.venv/bin/python scripts/validate_publication_bundle.py \
  reports/publication/qwen3-4b-strict-toolcall-v4-targeted \
  --require-ready
```

The future gate must fail until the remaining public-release checklist items are
checked with evidence.

## Next Actions

1. Decide whether to keep the current pilot-only standard benchmark positioning
   or run broader official suites on Azure or another suitable runtime.
2. Finalize the Hugging Face model card only after the release wording reflects
   the runtime prefill requirement and pilot-only benchmark scope.
3. Record human publication approval before changing private draft visibility.
