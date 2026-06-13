# Publish Readiness Checklist: Qwen3 4B Strict Tool-Call V6 Free-Text Copy

Date: 2026-06-13

## Local Quality Gates

- [x] Held-out strict local tool-call suite passes at `1.000`.
- [x] Mirrored regression suite passes at `1.000`.
- [x] Runtime condition recorded: `/no_think` plus assistant prefill.

## Public Release Gates

- [x] Dataset/source redistribution review complete for all materialized training rows.
- [ ] Standard benchmark stage target is met.
- [ ] Hugging Face model card finalized.
- [ ] Human publication approval recorded.

## Current Decision

Local promotion is approved for Hermes strict tool-call integration. Public
release is blocked pending model-card finalization, explicit human approval,
and benchmark-scope disclosure.
