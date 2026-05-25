# Publish Readiness: Qwen3 4B Strict Tool-Call V4 Targeted

Status: LOCAL STRICT GATE PASSED; PUBLIC HUGGING FACE PUBLICATION PENDING REVIEW

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
- [ ] Dataset/source redistribution review complete for all materialized training rows.
- [ ] Standard benchmark stage target is met.
- [ ] Hugging Face model card finalized.
- [ ] Human publication approval recorded.

## Decision

The V4 adapter satisfies the local strict held-out tool-call gate when evaluated
with the recorded assistant prefill. It is the first candidate in this project
to pass the strict gate at `1.000`.

The dataset overlap audit is valid and reproducible, with no held-out user
prompt overlap. It does show one held-out tool-name overlap
(`notify_care_team`), so it is evidence for review rather than a final
redistribution approval.

Public Hugging Face publication should still wait for the remaining publication
items above. In particular, the adapter was trained from materialized strict
tool-call rows that include earlier mirrored seed material, so the dataset/source
redistribution review must be completed before representing this as a public
release artifact.
