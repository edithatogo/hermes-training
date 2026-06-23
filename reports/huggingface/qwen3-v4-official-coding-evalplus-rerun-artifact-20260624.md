# Qwen3 v4 Official Coding EvalPlus Rerun HF Artifact

HF dataset repo: `edithatogo/hermes-training-artifacts`
Visibility target: `private`
Status: `blocked-auth`
Path prefix target: `qwen3-v4-official-coding-evalplus-rerun-20260624/`

The raw EvalPlus rerun evidence was staged locally at
`/tmp/qwen3-v4-official-coding-evalplus-rerun-20260624`, but the upload could
not be completed because the active shell is not authenticated with Hugging
Face.

## Upload Attempt

```bash
hf upload edithatogo/hermes-training-artifacts \
  /tmp/qwen3-v4-official-coding-evalplus-rerun-20260624 \
  qwen3-v4-official-coding-evalplus-rerun-20260624 \
  --repo-type dataset \
  --private \
  --commit-message 'Add Qwen3 v4 EvalPlus rerun evidence' \
  --json
```

Result: `401 Unauthorized`.

## Staged Files

- `report.json`
- `report.md`
- `generated.jsonl`
- `generated_eval_results.json`
- `generation-summary.json`
- `evalplus-humaneval-no-memlimit.log`

This is evidence-only material for a completed HumanEval/EvalPlus rerun. It is
not a broad model quality claim.
