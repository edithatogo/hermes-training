# Publish Readiness: Qwen3 4B Strict Tool-Call V5 Pilot Polish

Status: BLOCKED

Machine gate: NOT READY FOR PUBLIC RELEASE

## Gates

- [x] Structural readiness checks pass.
- [x] Training config recorded.
- [x] Training command recorded.
- [x] Training log recorded.
- [x] Adapter path recorded.
- [x] Dataset overlap audit recorded.
- [x] Dataset token audit recorded.
- [x] Runtime condition recorded: `/no_think` plus assistant prefill.
- [x] Mirrored regression suite passes at `1.000`.
- [x] BFCL-style pilot improves to `1.000`.
- [ ] Held-out strict local tool-call suite passes at `1.000`.
- [ ] Standard benchmark stage target is met for a release candidate.
- [ ] Hugging Face model card finalized.
- [ ] Human publication approval recorded.

## Decision

V5 is not publishable. The held-out strict local tool-call gate is `0.875`, below
the required `1.000`.

The experiment is still useful: it shows invalid-tool refusal examples can fix
the local BFCL-style pilot failure, but also that adding them without
argument-extraction retention data can regress a held-out argument case.
