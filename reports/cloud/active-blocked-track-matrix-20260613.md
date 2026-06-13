# Active Blocked Track Matrix

Registry: `conductor/tracks.md`
Unblock checklist: `reports/cloud/backend-unblock-checklist-20260613.json`

| Track | Backend | Backend status | Blocker | Next unchecked task |
|---|---|---|---|---|
| `qwen3-v4-peft-azure-scorecard_20260613` | `azure` | `blocked` | Azure CLI is installed but not currently logged in. | Complete `az login --use-device-code` for the student account. |
| `qwen3-v4-peft-colab-full-scorecard_20260613` | `colab` | `ready` | No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159. | Retry only after Colab keepalive permission is fixed or a persistent backend is selected. |
| `qwen3-v4-peft-colab-scorecard-shards_20260613` | `colab` | `ready` | No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159. | Re-run `truthfulqa_mc2` only after Colab keepalive permission is fixed or a persistent backend is selected. |
| `qwen3-v4-peft-hf-jobs-scorecard_20260613` | `hf_jobs` | `blocked-insufficient-hf-credits` | HF Jobs rejected the live route probe with insufficient prepaid credits. | Submit the job and capture job ID/log URL after credits/grant are available. |
| `qwen3-v4-peft-kaggle-scorecard_20260613` | `kaggle` | `blocked-needs-auth` | Kaggle CLI is installed but unauthenticated. | Authenticate the Kaggle CLI and check GPU quota. |
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
# after permission is fixed:
./.venv/bin/python scripts/colab_lm_eval_shard.py launch --config reports/benchmark/manifests/qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-config-20260613.json --session qwen3-v4-peft-colab-lm-eval-truthfulqa-mc2-full-20260613-retry3 --gpu T4
```

### qwen3-v4-peft-colab-scorecard-shards_20260613

```bash
PATH="$HOME/.local/bin:$PATH" colab sessions
./.venv/bin/python scripts/cloud_backend_preflight.py
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
kaggle auth login
kaggle quota
./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py
./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py --execute --confirm-kaggle-run
```

### qwen3-v4-peft-ngc-cloud-function-scorecard_20260613

```bash
ngc sso login
ngc config current
ngc cloud-function gpu quota
ngc cloud-function task create --help
```
