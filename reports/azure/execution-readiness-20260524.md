# Azure Execution Readiness

Date: 2026-05-24

## Current Policy

Azure remains fail-closed. Do not create workspaces, compute, endpoints, or jobs until all of these are true:

- active account is `d.a.mordaunt@gmail.com`
- subscription is `Azure for Students`
- selected region is recorded
- GPU quota is confirmed for the selected SKU family
- no-spend controls are accepted
- output paths resolve under `/Volumes/PortableSSD`
- first job is a minimal benchmark or teacher/evaluator smoke

## Local Templates

- `templates/azure/workspace.yaml`
- `templates/azure/compute-lowpri-t4.yaml`
- `templates/azure/compute-lowpri-a100.yaml`
- `templates/azure/benchmark-job.yaml`
- `templates/azure/teacher-evaluator-job.yaml`
- `templates/azure/cloud-run-card.md`

## First Allowed Live Action

The first live Azure action, after quota and no-spend evidence pass, should be a minimal benchmark or teacher/evaluator smoke. It should not be a training sweep.

## Publication Boundary

Azure outputs must be synced back to `/Volumes/PortableSSD` before any GitHub or Hugging Face claims are updated.

## Read-Only Preflight Result

Command:

```bash
source scripts/env.sh
./.venv/bin/python scripts/azure_preflight.py --check-quota --region australiaeast
```

Result on 2026-05-24:

- Azure CLI: present
- Active user: `d.a.mordaunt@gmail.com`
- Subscription: `Azure for Students`
- Subscription state: `Enabled`
- Azure ML CLI extension: installed
- SSD artifact root: `/Volumes/PortableSSD`
- Region checked: `australiaeast`
- Preflight status: account passed; quota checks still required before compute

GPU-family quota rows included nonzero legacy NC/NV family limits, but modern sampled GPU families needed for useful benchmark acceleration remained zero, including `NCASv3_T4`, `NCADS_A100_v4`, `NDASv4_A100`, and `NDSH100v5`. Keep Azure live execution blocked until a specific SKU/region quota is approved.

## Read-Only Status Result

Command:

```bash
source scripts/env.sh
./.venv/bin/python scripts/azure_status.py
```

Result on 2026-05-24:

- Providers registered: MachineLearningServices, Compute, Storage, KeyVault, ContainerRegistry, Insights
- Resource groups visible: `rg-powerplatform-payg-aue`, `rg-kairos-batch-canary-20260520`
- Azure ML workspaces: none
- Local templates present under `templates/azure/`

This confirms that no Azure ML workspace currently exists for this project. Workspace creation remains gated behind quota and no-spend controls.
