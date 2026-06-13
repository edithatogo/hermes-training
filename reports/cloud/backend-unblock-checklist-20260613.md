# Cloud Backend Unblock Checklist

Source preflight: `reports/cloud/backend-preflight-20260613.json`

This checklist is fail-closed. It records the next operator actions but does not run login, paid compute, or remote jobs.

## colab

- Status: `ready`
- Blocker: No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159.
- Operator actions:
  - Confirm `colab sessions` is empty or intentionally owned.
  - Fix Google Cloud service usage permission (`serviceusage.services.use`) for project 1014160490159 before another no-limit shard retry.
  - If that permission cannot be fixed, prefer a persistent backend instead of repeated Colab retries.
- Commands:

```bash
PATH="$HOME/.local/bin:$PATH" colab sessions
./.venv/bin/python scripts/cloud_backend_preflight.py
# after permission is fixed:
./.venv/bin/python scripts/colab_lm_eval_shard.py launch --config reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-config-20260613.json --session qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry3 --gpu T4
```

## hf_jobs

- Status: `blocked-insufficient-hf-credits`
- Blocker: HF Jobs rejected the live route probe with insufficient prepaid credits.
- Operator actions:
  - Add Hugging Face prepaid credits or grant capacity.
  - Keep paid GPU submission explicitly confirmation-gated.
  - Submit the prepared scorecard only after credits are visible.
- Commands:

```bash
hf jobs ps
./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py
./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py --execute --confirm-paid-compute
```

## azure

- Status: `blocked`
- Blocker: Azure CLI is installed but not currently logged in.
- Operator actions:
  - Run device-code login for the intended account.
  - Select `Azure for Students` if available.
  - Rerun quota checks before any workspace, compute, or job action.
- Commands:

```bash
az login --use-device-code
az account set --subscription "Azure for Students"
./.venv/bin/python scripts/azure_preflight.py --check-quota --region australiaeast
./.venv/bin/python scripts/azure_status.py
./.venv/bin/python scripts/submit_azure_peft_scorecard.py
./.venv/bin/python scripts/submit_azure_peft_scorecard.py --execute --confirm-azure-run
```

## ngc

- Status: `blocked`
- Blocker: NGC has no configured API key, SSO session, org/team, GPU quota, or benchmark container.
- Operator actions:
  - Authenticate with SSO or supplied API key without committing secrets.
  - Record non-secret org/team and Cloud Function GPU quota evidence.
  - Build or select an NGC registry benchmark container before any task submission.
- Commands:

```bash
ngc sso login
ngc config current
ngc cloud-function gpu quota
ngc cloud-function task create --help
```

## kaggle

- Status: `blocked-needs-auth`
- Blocker: Kaggle CLI is installed but unauthenticated.
- Operator actions:
  - Authenticate Kaggle CLI with OAuth or an API token.
  - Check weekly accelerator quota before pushing a kernel.
  - Push the staged kernel only after explicit confirmation.
- Commands:

```bash
kaggle auth login
kaggle quota
./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py
./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py --execute --confirm-kaggle-run
```
