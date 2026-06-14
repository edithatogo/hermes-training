# Cloud Backend Preflight Registry

Date: 2026-06-14T00:36:35.854414+00:00
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
| `colab` | `ready` | `primary; accelerators=gpu:T4,gpu:L4,gpu:A100,tpu:v5e1; tpu_opt_in=True` | no Colab CLI, command failure, active session not intentionally owned, or upload requires private data | Use scripts/colab_dispatch.py for bounded GPU-first jobs. Add --allow-tpu only for TPU-compatible adaptive scripts; PEFT lm-eval and MLX/llama.cpp scorecards stay GPU/persistent-backend only. |
| `hf_jobs` | `blocked-insufficient-hf-credits` | `persistent` | missing HF login, unavailable Jobs hardware, absent mounted artifacts, no result persistence, or no paid compute approval | Add HF prepaid credits or grant capacity, then submit with scripts/submit_hf_jobs_peft_scorecard.py --execute --confirm-paid-compute. |
| `azure` | `blocked` | `prepared` | missing login, wrong subscription, absent Azure ML extension, zero GPU quota, or no cost approval | Run az login only when the user is ready; then use scripts/azure_preflight.py before any job. |
| `ngc` | `blocked` | `prepared` | missing API key, org/team, entitlement, container access, model access, or license approval | Configure NGC only after the user supplies keys or completes SSO; then check Cloud Function GPU quota and registry access. |
| `kaggle` | `prepared-needs-notebook-contract` | `future` | missing CLI, missing credentials, dataset terms, private data, or unbounded notebook runtime | Add a fail-closed Kaggle notebook/job spec and dry-run it before any public dataset or GPU execution. |
| `modal` | `prepared-needs-credit-and-gpu-policy-check` | `container-serverless-candidate` | missing Modal token, unknown free credits/grant, no GPU policy proof, or no result persistence proof | Use Modal only after confirming free credits/grant and adding a fail-closed Modal scorecard submitter. |
| `lightning` | `blocked-needs-teamspace-owner` | `studio-job-candidate` | missing Lightning login, missing Teamspace owner, unknown free credits, no selected machine type, or no artifact recovery proof | Run lightning login if needed, configure the intended Teamspace owner, then rerun this preflight. |
