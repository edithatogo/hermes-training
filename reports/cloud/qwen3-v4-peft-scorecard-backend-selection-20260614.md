# Qwen3 v4 PEFT Scorecard Backend Selection

- Status: `blocked-pending-operator-gates`
- Execute: `false`
- Promotion allowed: `false`
- Selected backend: `kaggle`
- Selected backend status: `prepared-needs-run-approval`

Use the selected backend only after the listed operator gates pass. Do not retry Colab no-limit shards while keepalive/session-pruning blockers remain.

## Required Before Execution

- artifact recovery plan
- cost or zero-cost policy confirmation
- explicit run approval

## Ranked Backends

| Rank | Backend | Status | Score | Blocker |
|---:|---|---|---:|---|
| 1 | `kaggle` | `prepared-needs-run-approval` | 105 | Kaggle CLI, quota visibility, public-input notebook contract, and local result ingest gate are ready; remaining gates are explicit run approval and artifact recovery. |
| 2 | `modal` | `prepared-needs-credit-and-gpu-policy-check` | 75 | Modal CLI is authenticated; remaining gates are free credit/grant proof, GPU policy, and result persistence. |
| 3 | `hf_jobs` | `blocked-insufficient-hf-credits` | 25 | HF Jobs rejected the live route probe with insufficient prepaid credits. |
| 4 | `azure` | `blocked` | 5 | Azure CLI is installed but not currently logged in. |
| 5 | `colab` | `ready` | 5 | No-limit PEFT scorecards repeatedly prune or terminate after the Colab keepalive helper hits HTTP 403 for project 1014160490159. |
| 6 | `lightning` | `blocked-needs-teamspace-owner` | 5 | Lightning SDK is installed, but Studio/Job commands need login and a configured Teamspace owner. |
| 7 | `ngc` | `blocked` | 5 | NGC has no configured API key, SSO session, org/team, GPU quota, or benchmark container. |
