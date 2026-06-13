# Cloud Backend Preflight Registry

Date: 2026-06-13T03:45:16.255116+00:00
Storage root: `/Volumes/PortableSSD`
Storage root exists: `True`

## Policy

- `no_paid_compute_without_approval`: `True`
- `no_private_data_uploads`: `True`
- `no_model_or_dataset_publication`: `True`
- `artifact_root`: `/Volumes/PortableSSD/hermes-evals`
- `tracked_report_root`: `reports/cloud`

## Backends

| Backend | Status | Route | Stop condition | Next action |
|---|---|---|---|---|
| `colab` | `ready` | `primary` | no Colab CLI, command failure, active session not intentionally owned, or upload requires private data | Use scripts/colab_dispatch.py for bounded GPU-first jobs; update google-colab-cli when convenient. |
| `hf_jobs` | `prepared-needs-paid-compute-approval` | `persistent` | missing HF login, unavailable Jobs hardware, absent mounted artifacts, no result persistence, or no paid compute approval | Use HF Jobs for persistent no-limit scorecards only after explicit paid GPU approval. |
| `azure` | `blocked` | `prepared` | missing login, wrong subscription, absent Azure ML extension, zero GPU quota, or no cost approval | Run az login only when the user is ready; then use scripts/azure_preflight.py before any job. |
| `ngc` | `blocked` | `prepared` | missing API key, org/team, entitlement, container access, model access, or license approval | Configure NGC only after the user supplies keys; record non-secret org/team and entitlement proof. |
| `kaggle` | `blocked` | `future` | missing CLI, missing credentials, dataset terms, private data, or unbounded notebook runtime | Install and authenticate Kaggle CLI before adding Kaggle execution jobs. |
