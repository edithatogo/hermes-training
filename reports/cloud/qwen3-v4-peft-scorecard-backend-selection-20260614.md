# Qwen3 v4 PEFT Scorecard Backend Selection

- Status: `blocked-pending-operator-gates`
- Execute: `false`
- Promotion allowed: `false`
- Selected backend: `modal`
- Selected backend status: `prepared-needs-credit-and-gpu-policy-check`

Use the selected backend only after the listed operator gates pass. Do not retry Colab no-limit shards while keepalive/session-pruning blockers remain. Do not retry Kaggle unchanged after a failed live ingest.

## Required Before Execution

- artifact recovery plan
- cost or zero-cost policy confirmation
- explicit run approval

## Ranked Backends

| Rank | Backend | Status | Score | Blocker |
|---:|---|---|---:|---|
| 1 | `modal` | `prepared-needs-credit-and-gpu-policy-check` | 75 | Modal CLI is authenticated; remaining gates are free credit/grant proof, GPU policy, and result persistence. |
| 2 | `hf_jobs` | `blocked-insufficient-hf-credits` | 25 | HF Jobs rejected the live route probe with insufficient prepaid credits. |
| 3 | `azure` | `blocked` | 5 | Azure CLI is installed but not currently logged in. |
| 4 | `colab` | `ready` | 5 | No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159. |
| 5 | `lightning` | `blocked-needs-teamspace-owner` | 5 | Lightning SDK is installed, but Studio/Job commands need login and a configured Teamspace owner. |
| 6 | `ngc` | `blocked` | 5 | NGC has no configured API key, SSO session, org/team, GPU quota, or benchmark container. |
| 7 | `kaggle` | `running-needs-artifact-recovery` | -75 | Kaggle kernel version 5 has been submitted and is running; remaining gate is SSD artifact recovery plus no-pending ingest validation. Live Kaggle ingest failed after a completed kernel run; do not retry unchanged P100/CUDA path. |
