# Qwen3 V4 PEFT Lightning Scorecard Plan

Status: `blocked-needs-teamspace-owner`

## Rationale

Lightning Jobs may provide a persistent GPU route if login, Teamspace ownership,
machine availability, free credit/grant status, and artifact recovery are
confirmed. It is only a fallback to Colab pruning, HF Jobs credits, Kaggle
run approval, Modal policy, Azure login/quota, and NGC setup.

## Prepared Artifact

Guarded submitter:

```text
scripts/submit_lightning_peft_scorecard.py
```

Dry-run submission artifact:

```text
reports/cloud/qwen3-v4-peft-lightning-submit-dry-run-20260614.json
```

Staged config folder:

```text
reports/cloud/lightning-qwen3-v4-peft-scorecard-20260614
```

## Current Blocker

The preflight report records Lightning as blocked on Teamspace owner/login
setup. The dry-run keeps the Teamspace as `<owner>/<teamspace>` and does not
launch a job. No Lightning job was submitted.

## Stop Conditions

- No Lightning run without `--execute --confirm-lightning-run --confirm-zero-cost-compute`.
- No execution with the placeholder `<owner>/<teamspace>` Teamspace.
- No no-limit benchmark claim until every configured task completes without
  `--limit` and artifacts are recovered locally to the SSD.
