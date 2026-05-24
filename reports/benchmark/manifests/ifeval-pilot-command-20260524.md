# IFEval Pilot Command Manifest

Date: 2026-05-24

## Purpose

Run a low-cost instruction-following pilot for candidate models before any publication-oriented standardized evaluation.

## Gate

- Candidate runtime must be stable through a non-streaming OpenAI-compatible endpoint.
- Sampling must be deterministic enough for repeatability: `temperature=0`, fixed max tokens, no hidden prompt edits.
- Output root must be on `/Volumes/PortableSSD`.

## Command

```bash
source scripts/env.sh
RUN_ID=<model>-ifeval-pilot-<date>
MODEL_ID=<runtime_model_id>
BASE_URL=http://127.0.0.1:<port>/v1
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ifeval/${RUN_ID}
mkdir -p "$OUT"

python -m lm_eval \
  --model local-completions \
  --tasks ifeval \
  --limit 25 \
  --batch_size 1 \
  --output_path "$OUT"
```

The exact `lm_eval` model adapter must be resolved against the installed harness before execution. If the harness does not support the active endpoint adapter, record the adapter blocker instead of modifying scores manually.

## Result Card Schema

```json
{
  "run_id": "<model>-ifeval-pilot-<date>",
  "suite": "ifeval-pilot",
  "model": "<runtime_model_id>",
  "base_url": "http://127.0.0.1:<port>/v1",
  "limit": 25,
  "raw_output": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ifeval/<run-id>",
  "prompt_template": "suite-default",
  "strict_accuracy": null,
  "loose_accuracy": null,
  "publish_decision": "pilot-only"
}
```

## Publication Boundary

Pilot results are not leaderboard evidence. Publication requires full IFEval, harness version capture, raw outputs, normalized summaries, and failure examples.
