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
- [ ] Mirrored local tool-call regression result is recorded
- [ ] Held-out strict local tool-call benchmark passes at `1.000`
- [ ] Standard benchmark stage target is met
- [ ] Runtime smoke is documented for supported lanes
- [ ] License and redistribution notes are reviewed
- [ ] Human review is complete

Blocker:

Adapter publication remains blocked until `benchmarks/tool_call_local/heldout_suite.json` passes strictly at `1.000`. Do not create a Hugging Face repo or upload adapter files while this checklist says `Publication status: BLOCKED`.
