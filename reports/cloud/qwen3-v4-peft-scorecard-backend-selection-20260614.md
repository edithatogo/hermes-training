# Qwen3 v4 PEFT Scorecard Backend Selection

- Status: `blocked-pending-operator-gates`
- Execute: `false`
- Promotion allowed: `false`
- Selected backend: `kaggle`
- Selected backend status: `completed-validated-scorecard`

Use the recovered Kaggle v7 artifacts as the selected no-limit scorecard evidence. Keep any future remote execution behind the listed operator gates.

## Required Before Execution

- artifact recovery plan
- cost or zero-cost policy confirmation
- explicit run approval

## Ranked Backends

| Rank | Backend | Status | Score | Blocker |
|---:|---|---|---:|---|
| 1 | `kaggle` | `completed-validated-scorecard` | 105 | Kaggle kernel version 7 completed a no-limit five-task PEFT lm-eval scorecard; the SSD artifacts passed the no-pending ingest gate. No further Kaggle execution is required for this scorecard. |
| 2 | `modal` | `prepared-needs-credit-and-gpu-policy-check` | 75 | Modal CLI is authenticated; remaining gates are free credit/grant proof, GPU policy, and fail-closed result persistence. |
| 3 | `hf_jobs` | `blocked-insufficient-hf-credits` | 25 | HF Jobs rejected the live route probe with insufficient prepaid credits. |
| 4 | `azure` | `blocked` | 5 | Azure CLI is installed but not currently logged in. |
| 5 | `colab` | `ready` | 5 | No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159. |
| 6 | `lightning` | `blocked-needs-teamspace-owner` | 5 | Lightning SDK is installed, but Studio/Job commands need login and a configured Teamspace owner. |
| 7 | `ngc` | `blocked` | 5 | NGC has no configured API key, SSO session, org/team, GPU quota, or benchmark container. |
