# Publish Readiness Checklist

Publication status: BLOCKED

Target artifact:

- Adapter repo: `edithatogo/qwen3-4b-hermes-lora`
- Dataset repo: `edithatogo/hermes-training-data`
- Report directory: `reports/publication/qwen3-4b-smoke`
- Run card: `run-card.md`
- Model card draft: `hf-model-card-draft.md`
- Dataset card draft: `hf-dataset-card-draft.md`

Required gates:

- [x] Training run card is complete and exact
- [x] Dataset card is complete and exact for the smoke proof
- [x] Model card draft is complete and exact for the smoke proof
- [x] Exact benchmark command(s) are recorded
- [ ] Strict local tool-call benchmark passes
- [ ] Standard benchmark stage target is met
- [x] Runtime smoke is documented for supported lanes
- [x] License and redistribution notes are reviewed
- [x] Human review is complete for smoke documentation

Blocker:

Adapter publication remains blocked until the strict local tool-call benchmark passes. Do not create a Hugging Face repo or upload adapter files while this checklist says `Publication status: BLOCKED`.
