# Qwen3 V4 PEFT Kaggle Scorecard Plan

Status: `prepared-needs-notebook-contract`

## Rationale

Colab can run bounded pilots but has pruned no-limit sessions before artifacts
were recovered. HF Jobs is prepared but currently blocked by insufficient
prepaid credits. Kaggle Kernels is therefore a useful additional persistent lane
now that the CLI is authenticated, once accelerator quota and dataset terms are
confirmed.

## Prepared Artifact

Kernel runner:

```text
scripts/kaggle_peft_lm_eval_selected.py
```

Guarded submitter:

```text
scripts/submit_kaggle_peft_scorecard.py
```

Dry-run submission artifact:

```text
reports/cloud/qwen3-v4-peft-kaggle-submit-dry-run-20260613.json
```

Staged kernel folder:

```text
reports/cloud/kaggle-qwen3-v4-peft-scorecard-20260613
```

The staged kernel downloads the public PEFT adapter from:

```text
edithatogo/qwen3-4b-hermes-lora-peft-converted
```

and writes score artifacts under `/kaggle/working`.

## Candidate Command

```bash
kaggle kernels push \
  --path reports/cloud/kaggle-qwen3-v4-peft-scorecard-20260613 \
  --timeout 21600 \
  --accelerator gpu
```

The submitter will not push a Kaggle kernel unless both `--execute` and
`--confirm-kaggle-run` are provided.

## Current Blocker

`kaggle config view` now reports OAuth authentication for `edithatogo`, and
`kaggle kernels list --mine --page-size 1` returns successfully. The public
`kaggle quota` command currently fails with a CLI parsing error, but the
authenticated SDK fallback in `scripts/cloud_backend_preflight.py` returned GPU
quota `108000s` total / `0s` used and TPU quota `72000s` total / `0s` used,
refreshing at `2026-06-20T00:00:00Z`. The notebook contract passed in
`reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.md`: public inputs only,
no private data upload, GPU script metadata, no `--limit`, 21600s timeout, and
explicit `--execute --confirm-kaggle-run` operator boundary. No Kaggle notebook
was submitted and no GPU quota was consumed.

## Stop Conditions

- No Kaggle push until accelerator quota visibility and dataset terms are
  confirmed.
- No no-limit benchmark claim until every configured task completes without
  `--limit`.
- No private data upload; the staged kernel only uses public model artifacts and
  public code.
- No execution without explicit operator approval for
  `scripts/submit_kaggle_peft_scorecard.py --execute --confirm-kaggle-run`.
