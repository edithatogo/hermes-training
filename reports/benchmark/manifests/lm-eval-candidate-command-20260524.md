# lm-evaluation-harness Candidate Command Manifest

Date: 2026-05-24

## Purpose

Run a broader local comparability pass after a model clears runtime smoke and the local strict tool-call gate.

## Gate

- Candidate must have a stable endpoint or local adapter supported by `lm-evaluation-harness`.
- Candidate must have SSD-backed raw output roots.
- Candidate must have a run card with model revision, adapter revision, runtime version, prompt template, and sampling settings.

## Command

```bash
source scripts/env.sh
RUN_ID=<model>-lm-eval-candidate-<date>
MODEL_ID=<runtime_model_id>
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/${RUN_ID}
mkdir -p "$OUT"

python -m lm_eval \
  --model local-completions \
  --tasks arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande \
  --batch_size 1 \
  --output_path "$OUT"
```

Use the smoke manifest first with `LIMIT=10`. This candidate command is the next tier and should not run until adapter compatibility is confirmed.

## Result Card Schema

```json
{
  "run_id": "<model>-lm-eval-candidate-<date>",
  "suite": "lm-eval-candidate",
  "model": "<runtime_model_id>",
  "tasks": ["arc_challenge", "hellaswag", "truthfulqa_mc2", "gsm8k", "winogrande"],
  "raw_output": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/<run-id>",
  "harness_version": null,
  "normalized_scores": {},
  "known_failures": [],
  "publish_decision": "internal-candidate"
}
```

## Publication Boundary

Candidate results can inform model selection, but public claims require full harness metadata, deterministic rerun notes, and reviewer sign-off.
