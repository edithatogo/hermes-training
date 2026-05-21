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

For the Qwen3 strict-tool-call heldout promotion track, the publication folder is `reports/publication/qwen3-4b-strict-toolcall/`. Its checklist must stay BLOCKED until retraining on `gemma4/data/strict_tool_call` is complete and the heldout suite reports strict pass rate `1.000`.

Publish benchmark artifacts as either:

- files in the model repo under `eval/`, when small enough and license-compatible
- a separate Hugging Face dataset repo for larger raw generations/logs
- GitHub release artifacts when they are useful for reproducibility but too bulky for source control

## Current Publication Decision

As of 2026-05-22:

- GitHub: publish code, Conductor tracks, benchmark harnesses, run cards, model radar updates, and negative benchmark results. This work is reproducibility infrastructure and should be versioned now.
- Hugging Face dataset: defer until strict tool-call target examples are added, licensed, audited, and documented with a dataset card.
- Hugging Face adapter: do not publish the Qwen3 candidate adapter. It passed the response-collapse gate but failed the strict local tool-call benchmark, so publishing it would imply quality that the evidence does not support.
- Hugging Face GGUF/merged weights: do not publish merged Qwen3 artifacts unless the upstream license and redistribution path are explicitly reviewed and a runtime card passes.
- Publish-readiness checklist: keep adapter publication blocked until the held-out strict local tool-call benchmark passes; the checklist must record that blocker status directly.

Next publishable HF artifact should be either a cleaned tool-call dataset with a dataset card, or an adapter that beats base on the held-out local tool-call benchmark and has at least pilot-level standard benchmark results.
