# Cloud Backend Unblock Checklist

Source preflight: `reports/cloud/backend-preflight-20260613.json`

This checklist is fail-closed. It records the next operator actions but does not run login, paid compute, or remote jobs.

## colab

- Status: `ready`
- Blocker: No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159.
- Operator actions:
  - Confirm `colab sessions` is empty or intentionally owned.
  - Use the GPU ladder for PEFT lm-eval scorecards; do not route those scorecards to TPU.
  - Use `--allow-tpu` only for TPU-compatible adaptive scripts such as `scripts/colab_adaptive_train_smoke.py`.
  - Fix Google Cloud service usage permission (`serviceusage.services.use`) for project 1014160490159 before another no-limit shard retry.
  - If that permission cannot be fixed, prefer a persistent backend instead of repeated Colab retries.
- Accelerator policy:
  - Default ladder: `gpu:T4,gpu:L4,gpu:A100,tpu:v5e1`
  - TPU requires opt-in: `True`
  - TPU-compatible scripts: `scripts/colab_adaptive_train_smoke.py`
  - TPU-incompatible workloads: `MLX adapter scoring, PEFT lm-eval selected-task scorecards, llama.cpp/GGUF endpoint pilots`
- Commands:

```bash
PATH="$HOME/.local/bin:$PATH" colab sessions
./.venv/bin/python scripts/cloud_backend_preflight.py
# bounded GPU/TPU adaptive smoke, no scorecard claim:
./.venv/bin/python scripts/colab_dispatch.py --accelerators gpu:T4,gpu:L4,gpu:A100,tpu:v5e1 --allow-tpu --run-id colab-gpu-tpu-adaptive-smoke scripts/colab_adaptive_train_smoke.py
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
./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py
./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py --container-image <ngc-registry-image> --gpu-specification <gpu-spec> --execute --confirm-ngc-run
```

## kaggle

- Status: `completed-failed-needs-kaggle-runner-fix`
- Blocker: Kaggle kernel version 3 completed without scores; the NumPy-pinned runner contract now passes, but any further rerun requires explicit approval or rerouting.
- Operator actions:
  - Keep the recovered v2 and v3 failed summaries on the SSD as non-promotional evidence.
  - Use the passed staged runner contract as the baseline if another Kaggle rerun is explicitly approved.
  - Prefer a persistent backend such as Modal if cost/credit policy is cleared.
- Commands:

```bash
./.venv/bin/python scripts/validate_kaggle_rerun_submit_report.py
./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v2/qwen3-v4-peft-kaggle-lm-eval-20260613-233405-summary.json --no-allow-pending
./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-20260613-kernel-v3/qwen3-v4-peft-kaggle-lm-eval-20260613-234300-summary.json --no-allow-pending
./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py
```

## modal

- Status: `prepared-needs-credit-and-gpu-policy-check`
- Blocker: Modal CLI is authenticated; remaining gates are free credit/grant proof, GPU policy, and result persistence.
- Operator actions:
  - Confirm free credits, academic grant, or other zero-cost allowance before GPU execution.
  - Record non-secret GPU policy evidence for the intended workspace.
  - Add a fail-closed Modal scorecard submitter only after auth and result persistence are proven.
- Commands:

```bash
modal profile list
modal billing
./.venv/bin/python scripts/submit_modal_peft_scorecard.py
./.venv/bin/python scripts/submit_modal_peft_scorecard.py --execute --confirm-modal-run --confirm-zero-cost-compute
```

## lightning

- Status: `blocked-needs-teamspace-owner`
- Blocker: Lightning SDK is installed, but Studio/Job commands need login and a configured Teamspace owner.
- Operator actions:
  - Run Lightning login for the intended account.
  - Select or configure the Teamspace owner.
  - Confirm free monthly credits/GPU hours and a T4/L4 machine before adding a submitter.
- Commands:

```bash
lightning login
lightning studio list
lightning machine list
lightning job list
./.venv/bin/python scripts/submit_lightning_peft_scorecard.py
./.venv/bin/python scripts/submit_lightning_peft_scorecard.py --teamspace <owner>/<teamspace> --execute --confirm-lightning-run --confirm-zero-cost-compute
```
