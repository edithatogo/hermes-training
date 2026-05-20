# Azure ML GPU Quota Request Notes

## Current Subscription

- Account: `d.a.mordaunt@gmail.com`
- Subscription: `Azure for Students`
- Region checked: `australiaeast`
- Current useful GPU quotas:
  - `Standard NCASv3_T4 Family vCPUs`: `0`
  - `Standard NCADS_A100_v4 Family vCPUs`: `0`
  - `Standard NCadsH100v5 Family vCPUs`: `0`
  - `Standard NDSH100v5 Family vCPUs`: `0`
- Low-priority regional vCPU quota observed: `3`
- Total regional vCPU quota observed: `6`

## Minimum Useful Requests

For cost-first smoke benchmarks:

- Quota type: Azure Machine Learning VM family quota
- Region: `australiaeast` unless another region has better availability
- VM family: `NCASv3_T4`
- Requested limit: at least `4` vCPUs for `Standard_NC4as_T4_v3`
- Justification: short-lived benchmark smoke and teacher/evaluator jobs for Hermes local-model research, max one low-priority node, scale-to-zero when idle.

For larger teacher/evaluator runs:

- VM family: `NCADS_A100_v4`
- Requested limit: at least `24` vCPUs for `Standard_NC24ads_A100_v4`
- Justification: occasional larger-model evaluation only after T4 smoke path is proven.

## Request Guidance

Microsoft documents that specialized GPU families such as `NCasT4_v3` and `NC_A100_v4` often start with zero quota, and quota is not a capacity guarantee. Request quota in Azure ML Studio or Azure portal before creating compute.

References:

- https://learn.microsoft.com/azure/machine-learning/how-to-manage-quotas
- https://learn.microsoft.com/azure/quotas/quickstart-increase-quota-portal
