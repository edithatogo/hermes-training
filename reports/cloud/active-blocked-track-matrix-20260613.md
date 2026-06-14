# Active Blocked Track Matrix

Registry: `conductor/tracks.md`
Unblock checklist: `reports/cloud/backend-unblock-checklist-20260613.json`

| Track | Backend | Backend status | Blocker | Next unchecked task |
|---|---|---|---|---|
| `qwen3-v4-peft-azure-scorecard_20260613` | `azure` | `blocked` | Azure CLI is installed but not currently logged in. | Complete `az login --use-device-code` for the student account. |
| `qwen3-v4-peft-colab-full-scorecard_20260613` | `colab` | `ready` | No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159. | Retry only after Colab keepalive permission is fixed or a persistent backend is selected. |
| `qwen3-v4-peft-colab-scorecard-shards_20260613` | `colab` | `ready` | No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159. | Re-run `truthfulqa_mc2` only after Colab keepalive permission is fixed or a persistent backend is selected. |
| `qwen3-v4-peft-hf-jobs-scorecard_20260613` | `hf_jobs` | `blocked-insufficient-hf-credits` | HF Jobs rejected the live route probe with insufficient prepaid credits. | Submit the job and capture job ID/log URL after credits/grant are available. |
| `qwen3-v4-peft-kaggle-scorecard_20260613` | `kaggle` | `completed-failed-needs-kaggle-runner-fix` | Kaggle kernel version 4 completed without scores; the recovered summary is blocked, and this P100 path now needs a runner/runtime change or a different backend. | Route the full scorecard to a different backend or change the Kaggle runner/runtime strategy before any further rerun. |
| `qwen3-v4-peft-lightning-scorecard_20260614` | `lightning` | `blocked-needs-teamspace-owner` | Lightning SDK is installed, but Studio/Job commands need login and a configured Teamspace owner. | Run Lightning login and identify a real Teamspace only after explicit user approval. |
| `qwen3-v4-peft-modal-scorecard_20260614` | `modal` | `prepared-needs-credit-and-gpu-policy-check` | Modal CLI is authenticated; remaining gates are free credit/grant proof, GPU policy, and result persistence. | Confirm free credit/grant or zero-cost GPU policy. |
| `qwen3-v4-peft-ngc-cloud-function-scorecard_20260613` | `ngc` | `blocked` | NGC has no configured API key, SSO session, org/team, GPU quota, or benchmark container. | Configure NGC auth only after the user supplies keys or completes SSO. |

## Commands

### qwen3-v4-peft-azure-scorecard_20260613

```bash
az login --use-device-code
az account set --subscription "Azure for Students"
./.venv/bin/python scripts/azure_preflight.py --check-quota --region australiaeast
./.venv/bin/python scripts/azure_status.py
./.venv/bin/python scripts/submit_azure_peft_scorecard.py
./.venv/bin/python scripts/submit_azure_peft_scorecard.py --execute --confirm-azure-run
```

### qwen3-v4-peft-colab-full-scorecard_20260613

```bash
PATH="$HOME/.local/bin:$PATH" colab sessions
./.venv/bin/python scripts/cloud_backend_preflight.py
# bounded GPU/TPU adaptive smoke, no scorecard claim:
./.venv/bin/python scripts/colab_dispatch.py --accelerators gpu:T4,gpu:L4,gpu:A100,tpu:v5e1 --allow-tpu --run-id colab-gpu-tpu-adaptive-smoke scripts/colab_adaptive_train_smoke.py
# after permission is fixed:
./.venv/bin/python scripts/colab_lm_eval_shard.py launch --config reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-config-20260613.json --session qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry3 --gpu T4
```

### qwen3-v4-peft-colab-scorecard-shards_20260613

```bash
PATH="$HOME/.local/bin:$PATH" colab sessions
./.venv/bin/python scripts/cloud_backend_preflight.py
# bounded GPU/TPU adaptive smoke, no scorecard claim:
./.venv/bin/python scripts/colab_dispatch.py --accelerators gpu:T4,gpu:L4,gpu:A100,tpu:v5e1 --allow-tpu --run-id colab-gpu-tpu-adaptive-smoke scripts/colab_adaptive_train_smoke.py
# after permission is fixed:
./.venv/bin/python scripts/colab_lm_eval_shard.py launch --config reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-config-20260613.json --session qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry3 --gpu T4
```

### qwen3-v4-peft-hf-jobs-scorecard_20260613

```bash
hf jobs ps
./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py
./.venv/bin/python scripts/submit_hf_jobs_peft_scorecard.py --execute --confirm-paid-compute
```

### qwen3-v4-peft-kaggle-scorecard_20260613

```bash
./.venv/bin/python scripts/validate_kaggle_rerun_submit_report.py
./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v4-20260614/qwen3-v4-peft-kaggle-lm-eval-20260613-235158-summary.json --no-allow-pending
kaggle kernels output edithatogo/qwen3-v4-peft-lm-eval-selected-full --path /Volumes/PortableSSD/hermes-evals/kaggle/qwen3-v4-peft-lm-eval-selected-full-p100-v4-20260614
./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py
```

### qwen3-v4-peft-lightning-scorecard_20260614

```bash
lightning login
lightning studio list
lightning machine list
lightning job list
./.venv/bin/python scripts/submit_lightning_peft_scorecard.py
./.venv/bin/python scripts/submit_lightning_peft_scorecard.py --teamspace <owner>/<teamspace> --execute --confirm-lightning-run --confirm-zero-cost-compute
```

### qwen3-v4-peft-modal-scorecard_20260614

```bash
modal profile list
modal billing
./.venv/bin/python scripts/submit_modal_peft_scorecard.py
./.venv/bin/python scripts/submit_modal_peft_scorecard.py --execute --confirm-modal-run --confirm-zero-cost-compute
```

### qwen3-v4-peft-ngc-cloud-function-scorecard_20260613

```bash
ngc sso login
ngc config current
ngc cloud-function gpu quota
ngc cloud-function task create --help
./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py
./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py --container-image <ngc-registry-image> --gpu-specification <gpu-spec> --execute --confirm-ngc-run
```
