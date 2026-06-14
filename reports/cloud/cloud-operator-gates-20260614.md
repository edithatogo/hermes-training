# Cloud Operator Gates

Source checklist: `reports/cloud/backend-unblock-checklist-20260613.json`

This report is fail-closed. It records external evidence needed before cloud execution or promotion.

## colab

- Status: `ready`
- Execution allowed: `False`
- Promotion allowed: `False`
- Blocker: No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159.
- External evidence required:
  - Colab keepalive/serviceusage permission fixed for project 1014160490159
  - No active session conflict or intentionally owned session
  - Recovered no-limit lm-eval artifacts
- Safe commands:

```bash
PATH="$HOME/.local/bin:$PATH" colab sessions
./.venv/bin/python scripts/cloud_backend_preflight.py
# bounded GPU/TPU adaptive smoke, no scorecard claim:
./.venv/bin/python scripts/colab_dispatch.py --accelerators gpu:T4,gpu:L4,gpu:A100,tpu:v5e1 --allow-tpu --run-id colab-gpu-tpu-adaptive-smoke scripts/colab_adaptive_train_smoke.py
# after permission is fixed:
./.venv/bin/python scripts/colab_lm_eval_shard.py launch --config reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-config-20260613.json --session qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry3 --gpu T4
```

- Secret policy: Do not commit tokens, secrets, payment card details, private account IDs, or screenshots containing secrets.

## hf_jobs

- Status: `blocked-insufficient-hf-credits`
- Execution allowed: `False`
- Promotion allowed: `False`
- Blocker: HF Jobs rejected the live route probe with insufficient prepaid credits.
- External evidence required:
  - HF prepaid credits or grant capacity visible
  - Explicit paid-compute approval for selected hardware
  - Job ID/log URL and recovered Hub result artifacts
- Safe commands:

```bash
hf jobs ps
./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py
./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py --execute --confirm-paid-compute
```

- Secret policy: Do not commit tokens, secrets, payment card details, private account IDs, or screenshots containing secrets.

## azure

- Status: `blocked`
- Execution allowed: `False`
- Promotion allowed: `False`
- Blocker: Azure CLI is installed but not currently logged in.
- External evidence required:
  - Azure login to the intended student account
  - Azure for Students subscription selected
  - GPU quota/workspace/compute/environment preflight passed
  - Cost approval or zero-cost grant evidence
- Safe commands:

```bash
az login --use-device-code
az account set --subscription "Azure for Students"
./.venv/bin/python scripts/azure_preflight.py --check-quota --region australiaeast
./.venv/bin/python scripts/azure_status.py
./.venv/bin/python scripts/submit_azure_peft_scorecard.py
./.venv/bin/python scripts/submit_azure_peft_scorecard.py --execute --confirm-azure-run
```

- Secret policy: Do not commit tokens, secrets, payment card details, private account IDs, or screenshots containing secrets.

## ngc

- Status: `blocked`
- Execution allowed: `False`
- Promotion allowed: `False`
- Blocker: NGC has no configured API key, SSO session, org/team, GPU quota, or benchmark container.
- External evidence required:
  - NGC auth or SSO configured without committed secrets
  - Org/team and Cloud Function GPU quota evidence
  - Benchmark container image available in an accessible registry
- Safe commands:

```bash
ngc sso login
ngc config current
ngc cloud-function gpu quota
ngc cloud-function task create --help
./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py
./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py --container-image <ngc-registry-image> --gpu-specification <gpu-spec> --execute --confirm-ngc-run
```

- Secret policy: Do not commit tokens, secrets, payment card details, private account IDs, or screenshots containing secrets.

## kaggle

- Status: `running-needs-artifact-recovery`
- Execution allowed: `False`
- Promotion allowed: `False`
- Blocker: Kaggle kernel version 7 has been submitted and is running; remaining gate is SSD artifact recovery plus no-pending ingest validation.
- External evidence required:
  - Kernel completed
  - Artifacts recovered to /Volumes/PortableSSD
  - No-pending result ingest validation passed before any claim
- Safe commands:

```bash
./.venv/bin/python scripts/sync_kaggle_rerun_status.py
./.venv/bin/python scripts/sync_kaggle_rerun_status.py --recover-artifacts --artifact-dir /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v7-20260614
./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json <downloaded-summary> --no-allow-pending
```

- Secret policy: Do not commit tokens, secrets, payment card details, private account IDs, or screenshots containing secrets.

## modal

- Status: `prepared-needs-credit-and-gpu-policy-check`
- Execution allowed: `False`
- Promotion allowed: `False`
- Blocker: Modal CLI is authenticated; remaining gates are free credit/grant proof, GPU policy, and fail-closed result persistence.
- External evidence required:
  - Free credit, academic grant, or explicit paid-compute approval recorded in reports/cloud/modal-policy-evidence-20260614.json
  - Modal policy gate reports execution_allowed=true
  - Explicit Modal run approval
  - Post-run Modal result ingest validation
- Safe commands:

```bash
modal profile list
modal billing report --for "this month" --json
./.venv/bin/python scripts/validate_modal_policy_gate.py
./.venv/bin/python scripts/submit_modal_peft_scorecard.py
./.venv/bin/python scripts/submit_modal_peft_scorecard.py --execute --confirm-modal-run --confirm-zero-cost-compute
```

- Secret policy: Do not commit tokens, secrets, payment card details, private account IDs, or screenshots containing secrets.

## lightning

- Status: `blocked-needs-teamspace-owner`
- Execution allowed: `False`
- Promotion allowed: `False`
- Blocker: Lightning SDK is installed, but Studio/Job commands need login and a configured Teamspace owner.
- External evidence required:
  - Lightning login and Teamspace owner configured
  - Free credit/grant or explicit paid-compute approval
  - Selected machine policy and artifact recovery path proven
- Safe commands:

```bash
lightning login
lightning studio list
lightning machine list
lightning job list
./.venv/bin/python scripts/submit_lightning_peft_scorecard.py
./.venv/bin/python scripts/submit_lightning_peft_scorecard.py --teamspace <owner>/<teamspace> --execute --confirm-lightning-run --confirm-zero-cost-compute
```

- Secret policy: Do not commit tokens, secrets, payment card details, private account IDs, or screenshots containing secrets.
