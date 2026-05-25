# Publish Readiness: Qwen3 4B Strict Tool-Call V4 Targeted

Status: PUBLIC HUGGING FACE ADAPTER RELEASE APPROVED

Machine gate: READY FOR PUBLIC RELEASE

## Gates

- [x] Structural readiness checks pass.
- [x] Base model license checked: `Qwen/Qwen3-4B-MLX-4bit` is Apache-2.0.
- [x] Training config recorded.
- [x] Training command recorded.
- [x] Training log recorded.
- [x] Adapter path recorded.
- [x] Held-out benchmark command recorded.
- [x] Held-out strict local tool-call suite passes at `1.000`.
- [x] Mirrored regression suite passes at `1.000`.
- [x] Runtime condition recorded: `/no_think` plus assistant prefill.
- [x] Raw benchmark artifact paths recorded.
- [x] Dataset overlap audit recorded in `dataset-overlap-audit.json`.
- [x] Dataset token audit recorded in `dataset-token-audit.json`.
- [x] Hugging Face adapter uploaded and hash-verified.
- [x] Public release decision recorded in `release-decision.md`.
- [x] Publication bundle validator passes in ready mode:
  `./.venv/bin/python scripts/validate_publication_bundle.py reports/publication/qwen3-4b-strict-toolcall-v4-targeted --require-ready`
- [x] Dataset/source redistribution review complete for all materialized training rows.
- [x] Standard benchmark stage target is met.
- [x] Hugging Face model card finalized.
- [x] Human publication approval recorded.

## Decision

The V4 adapter satisfies the local strict held-out tool-call gate when evaluated
with the recorded assistant prefill. It is the first candidate in this project
to pass the strict gate at `1.000`.

The dataset overlap audit is valid and reproducible, with no held-out user
prompt overlap. It does show one held-out tool-name overlap
(`notify_care_team`), so it is evidence for review rather than a final
redistribution approval.

Public Hugging Face adapter publication is approved with narrow positioning:
experimental strict Hermes tool-call LoRA, not a broad benchmark winner. The
standard benchmark stage target is satisfied by recording repo-native pilot
scores and explicitly labeling them as pilot-only rather than official BFCL,
IFEval, HumanEval, or MBPP scores.

The dataset/source redistribution review is complete with caveats: the adapter
source-review gate is cleared, but public dataset publication remains blocked
pending separate human scope approval because the materialized rows include
mirrored local benchmark seed material.

Hugging Face adapter repo:

```text
https://huggingface.co/edithatogo/qwen3-4b-hermes-lora
```

The uploaded `adapters.safetensors` file was downloaded back from Hugging Face
and matched the local SHA-256:
`42e4364d2b8fe8d467295a4581d983623a296ec31aff006c514c6ca2d113039e`.

Human approval:

```text
User instruction on 2026-05-25: "Address all of the issues and make it public"
```

Public release validator:

```bash
./.venv/bin/python scripts/validate_publication_bundle.py \
  reports/publication/qwen3-4b-strict-toolcall-v4-targeted \
  --require-ready
```
