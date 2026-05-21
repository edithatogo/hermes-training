# Publish Readiness Checklist

Publication status: BLOCKED

Target artifact:

- Adapter repo:
- Dataset repo:
- Report directory:
- Run card:
- Model card draft:
- Dataset card draft:

Required gates:

- [ ] Training run card is complete and exact
- [ ] Dataset card is complete and exact
- [ ] Model card draft is complete and exact
- [ ] Exact benchmark command(s) are recorded
- [ ] Strict local tool-call benchmark passes
- [ ] Standard benchmark stage target is met
- [ ] Runtime smoke is documented for supported lanes
- [ ] License and redistribution notes are reviewed
- [ ] Human review is complete

Blocker:

Adapter publication remains blocked until the strict local tool-call benchmark passes. Do not create a Hugging Face repo or upload adapter files while this checklist says `Publication status: BLOCKED`.
