# Documentation Plan

## Required Docs Before Each Adapter Release

Each adapter candidate needs:

- Training run card: base model, config, dataset version, token count, hardware, runtime, elapsed time, peak memory, exact benchmark command(s), harness version/commit, prompt-set revision or hash
- Dataset card: source, filters, split counts, token counts, known limitations
- Evaluation report: Hermes-local benchmark, standardized benchmark suite, raw outputs, scores, manual review notes, score provenance for every published number
- Runtime card: MLX, Ollama, and LM Studio instructions where supported
- Publishing card: GitHub commit, Hugging Face repo, license and redistribution notes

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

Publish benchmark artifacts as either:

- files in the model repo under `eval/`, when small enough and license-compatible
- a separate Hugging Face dataset repo for larger raw generations/logs
- GitHub release artifacts when they are useful for reproducibility but too bulky for source control
