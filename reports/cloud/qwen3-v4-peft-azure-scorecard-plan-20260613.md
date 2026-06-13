# Qwen3 V4 PEFT Azure Scorecard Plan

Status: `blocked-not-logged-in`

## Purpose

Azure ML is the next persistent backend candidate for the Qwen3 v4 PEFT
no-limit selected-task `lm_eval[hf]` scorecard. Colab proved the PEFT route at
`--limit 5` but pruned no-limit runs before artifacts could be recovered. HF
Jobs is prepared but blocked by insufficient prepaid credits.

## Prepared Files

| Item | Path |
|---|---|
| Azure submitter | `scripts/submit_azure_peft_scorecard.py` |
| Azure job template | `templates/azure/qwen3-v4-peft-lm-eval-job.yaml` |
| Dry-run JSON | `reports/cloud/qwen3-v4-peft-azure-submit-dry-run-20260613.json` |
| Track | `conductor/tracks/qwen3-v4-peft-azure-scorecard_20260613/` |

## Dry-Run Result

| Field | Value |
|---|---|
| Status | `blocked` |
| Azure CLI | installed |
| Azure ML extension | `2.42.0` |
| Job template exists | `true` |
| Active account | blocked |
| Blocker | `ERROR: Please run 'az login' to setup account.` |

Prepared command:

```bash
az ml job create \
  --file /Volumes/PortableSSD/GitHub/hermes-training/templates/azure/qwen3-v4-peft-lm-eval-job.yaml \
  --resource-group hermes-ml-rg \
  --workspace-name hermes-ml-lab \
  --set name=qwen3-v4-peft-azure-lm-eval-selected-full-20260613 \
  compute=azureml:hermes-lowpri-t4
```

Guarded submitter command after login, quota, workspace, compute, environment,
and cost gates pass:

```bash
source scripts/env.sh
./.venv/bin/python scripts/submit_azure_peft_scorecard.py --execute --confirm-azure-run
```

## Claim Boundary

No full benchmark claim can be made from this plan. The `lm-eval-selected`
coverage remains blocked until Azure or another persistent backend completes all
selected tasks without `--limit` and the artifacts are downloaded to
`/Volumes/PortableSSD`.
