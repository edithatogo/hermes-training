# Documentation Plan

## Required Docs Before Each Adapter Release

Each adapter candidate needs:

- Training run card: base model, config, dataset version, token count, hardware, runtime, elapsed time, peak memory, exact benchmark command(s), harness version/commit, prompt-set revision or hash
- Dataset card: source, filters, split counts, token counts, known limitations
- Evaluation report: Hermes-local benchmark, standardized benchmark suite, raw outputs, scores, manual review notes, score provenance for every published number
- Runtime card: MLX, Ollama, and LM Studio instructions where supported
- Publishing card: GitHub commit, Hugging Face repo, license and redistribution notes
- Publish-readiness checklist: explicit gate status, exact mirrored and held-out tool-call benchmark results, and the blocker that prevents adapter publication until the held-out strict gate passes

## Repo-Level Docs

Maintain these files:

- `README.md`: current recommended path and commands
- `MODEL_CANDIDATES.yaml`: model radar and status
- `BENCHMARKING_PLAN.md`: gates, metrics, and promotion rule
- `STANDARD_BENCHMARKS.md`: standardized benchmark matrix for GitHub/Hugging Face reporting
- `DOCUMENTATION_PLAN.md`: release documentation requirements
- `HANDOFF.md`: current implementation state and next action
- `REPO_MAINTENANCE.md`: commit/push and artifact policy

## Run Notes Format

For every training run, create an ignored or publishable run note:

```markdown
# Run: <model>-<date>-<profile>

- Base model:
- Adapter path:
- Config:
- Dataset version:
- Train tokens:
- Iterations:
- Batch / grad accumulation:
- Max sequence length:
- Peak memory:
- Result:
- Benchmark summary:
- Standard benchmark status:
- Known issues:
- Next decision:
```

Keep local scratch run notes under ignored `experiments/`. Promote only clean, reviewed summaries into repo docs.

## Hugging Face Publishing Plan

Publish only after benchmark promotion:

- Dataset repo: `edithatogo/hermes-training-data`
- Adapter repos:
  - `edithatogo/lfm25-1.2b-hermes-lora`
  - `edithatogo/qwen3-4b-hermes-lora`
  - future model-specific repos as candidates pass

Each Hugging Face model card should include the training config, dataset card link, evaluation table, runtime commands, intended use, limitations, and license notes.
When a card cites benchmark numbers, include the exact command, model revision, harness version, prompt-set revision or hash, and the raw artifact location that produced the number.
Adapter publication stays blocked until `benchmarks/tool_call_local/heldout_suite.json` passes strictly at `1.000` and the publish-readiness checklist is marked READY. The mirrored `benchmarks/tool_call_local/suite.json` can support regression notes but cannot satisfy the held-out publication gate.

For the completed Qwen3 strict-tool-call heldout promotion attempt, the publication folder is `reports/publication/qwen3-4b-strict-toolcall/` and remains BLOCKED because strict held-out pass rate was below `1.000`.

For the completed expanded-data retrain attempt, the publication folder is `reports/publication/qwen3-4b-strict-toolcall-expanded/`. Its checklist remains BLOCKED because the heldout suite reported strict pass rate `0.250`, below the required `1.000`. Dataset token audit and license review are recorded, but the license review keeps Hugging Face publication blocked pending upstream and mirrored-seed redistribution approval.

For the completed v2/v3 strict format-guard attempts, the publication folder is `reports/publication/qwen3-4b-strict-toolcall-v2-v3/`. Its checklist remains BLOCKED because both v2 and v3 heldout suites reported strict pass rate `0.250`, below the required `1.000`. The v3 diagnostic empty-think-stripped score improved to `0.875`, but diagnostic normalization is integration evidence only and cannot replace the strict publication gate.

For the completed v4 targeted strict-tool-call attempt, the publication folder is `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/`. Its checklist records the first local strict held-out pass at `1.000`, using the required Qwen runtime condition: `/no_think` on the first user turn plus assistant prefill `<think>\n\n</think>\n\n`. Public Hugging Face adapter publication is approved as an experimental strict Hermes tool-call LoRA with pilot-only benchmark positioning. Public dataset publication remains separate and blocked pending scope approval.

For the completed v5 pilot-polish attempt, the publication folder is `reports/publication/qwen3-4b-strict-toolcall-v5-pilot-polish/`. Its checklist remains BLOCKED because the held-out strict local tool-call suite regressed to `0.875`, even though the BFCL-style pilot improved to `1.000`. Treat it as negative evidence and keep the v4 targeted adapter as the recommended/public adapter.

Publish benchmark artifacts as either:

- files in the model repo under `eval/`, when small enough and license-compatible
- a separate Hugging Face dataset repo for larger raw generations/logs
- GitHub release artifacts when they are useful for reproducibility but too bulky for source control

## Current Publication Decision

As of 2026-05-25:

- GitHub: publish code, Conductor tracks, benchmark harnesses, run cards, model radar updates, passing strict-gate evidence, and negative benchmark results. This work is reproducibility infrastructure and should be versioned now.
- Hugging Face dataset: defer until the expanded and targeted strict tool-call examples have accepted publication scope and final redistribution approval.
- Hugging Face adapter: the Qwen3 v4 targeted adapter passes the local strict held-out gate at `1.000` under the recorded runtime condition and is public as an experimental adapter release at `edithatogo/qwen3-4b-hermes-lora`.
- Hugging Face GGUF/merged weights: do not publish merged Qwen3 artifacts unless the upstream license and redistribution path are explicitly reviewed and a runtime card passes.
- Publish-readiness checklist: the v4 targeted adapter checklist is READY for public adapter release; the v5 pilot-polish checklist is BLOCKED and must not replace v4; continue to keep public dataset and merged-weight releases separate.

Next publishable HF artifact should be either a cleaned tool-call dataset with a dataset card, or the v4 targeted adapter after the remaining release gates are closed.
