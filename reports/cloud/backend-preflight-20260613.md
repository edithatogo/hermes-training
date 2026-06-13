# Cloud Backend Preflight Registry

Date: 2026-06-13T03:59:15.688982+00:00
Storage root: `/Volumes/PortableSSD`
Storage root exists: `True`

## Policy

- `no_paid_compute_without_approval`: `True`
- `no_private_data_uploads`: `True`
- `no_unreviewed_model_or_dataset_publication`: `True`
- `artifact_root`: `/Volumes/PortableSSD/hermes-evals`
- `tracked_report_root`: `reports/cloud`

## Backends

| Backend | Status | Route | Stop condition | Next action |
|---|---|---|---|---|
| `colab` | `ready` | `primary` | no Colab CLI, command failure, active session not intentionally owned, or upload requires private data | Use scripts/colab_dispatch.py for bounded GPU-first jobs; update google-colab-cli when convenient. |
| `hf_jobs` | `blocked-insufficient-hf-credits` | `persistent` | missing HF login, unavailable Jobs hardware, absent mounted artifacts, no result persistence, or no paid compute approval | Add HF prepaid credits or grant capacity, then submit with scripts/submit_hf_jobs_peft_scorecard.py --execute --confirm-paid-compute. |
| `azure` | `blocked` | `prepared` | missing login, wrong subscription, absent Azure ML extension, zero GPU quota, or no cost approval | Run az login only when the user is ready; then use scripts/azure_preflight.py before any job. |
| `ngc` | `blocked` | `prepared` | missing API key, org/team, entitlement, container access, model access, or license approval | Configure NGC only after the user supplies keys or completes SSO; then check Cloud Function GPU quota and registry access. |
| `kaggle` | `blocked-needs-auth` | `future` | missing CLI, missing credentials, dataset terms, private data, or unbounded notebook runtime | Authenticate Kaggle CLI with kaggle auth login or API token, then rerun this preflight. |
