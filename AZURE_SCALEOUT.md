# Azure Scale-Out

Azure is a scale-out lane for Hermes-agent benchmarks, teacher/evaluator runs, dataset review, and selected larger experiments.

## Default Policy

- Account target: `d.a.mordaunt@gmail.com`
- Subscription target: `Azure for Students`
- Initial region: `australiaeast`, with region changes allowed for GPU quota/capacity
- Cost posture: Spot/low-priority where available
- Compute posture: `min_instances: 0`, `max_instances: 1`
- First use: benchmark and teacher/evaluator runs, not broad training sweeps

## Preflight

Run from the hub:

```bash
source scripts/env.sh
./.venv/bin/python scripts/azure_preflight.py
```

The preflight is read-only. It checks Azure CLI login state, expected account/subscription, Azure ML CLI extension presence, SSD artifact root, and declared cost policy. It does not create compute or submit jobs.

After the student account is active, add quota inspection:

```bash
./.venv/bin/python scripts/azure_preflight.py --check-quota --region australiaeast
```

## Login Shape

Use device-code login when switching accounts:

```bash
az login --use-device-code
az account set --subscription "Azure for Students"
```

Then rerun preflight.

## Before Creating Compute

- Confirm GPU quota for the selected region and VM family.
- `az vm list-usage --location australiaeast` may not show Azure ML GPU-family quota rows for this subscription; confirm Azure ML workspace quota/capacity in Azure ML or the Azure portal before creating compute.
- Prefer T4/L40S/A100/H100 families based on task size and quota.
- Use benchmark-only smoke jobs before training jobs.
- Sync reports and artifacts back to `/Volumes/PortableSSD`.

## Read-Only Status

Run:

```bash
./.venv/bin/python scripts/azure_status.py
```

This reports the active account, provider registration state, resource groups, Azure ML workspaces, and available Azure templates without creating resources.

## Creation Templates

- `templates/azure/workspace.yaml`
- `templates/azure/compute-lowpri-t4.yaml`
- `templates/azure/compute-lowpri-a100.yaml`
- `templates/azure/quota-request.md`

Do not create the workspace until provider registration is complete and you accept that Azure ML workspace creation also creates supporting resources such as Storage, Key Vault, Container Registry, and Application Insights. Do not create compute until Azure ML GPU quota/capacity is confirmed.

## Current Quota Finding

Read-only quota inspection for `australiaeast` shows zero quota for the modern GPU families needed by the prepared templates:

- `Standard NCASv3_T4 Family vCPUs`: `0`
- `Standard NCADS_A100_v4 Family vCPUs`: `0`
- `Standard NCadsH100v5 Family vCPUs`: `0`
- `Standard NDSH100v5 Family vCPUs`: `0`

The subscription has small legacy `Standard NC Family` and `Standard NV Family` quotas, but those are not the target path for current Hermes benchmark/teacher work. Use `templates/azure/quota-request.md` before creating compute.

## Skeleton Templates

- `templates/azure/benchmark-job.yaml`
- `templates/azure/teacher-evaluator-job.yaml`
- `templates/azure/cloud-run-card.md`

These are non-spending skeleton artifacts only. They document the cost-first defaults and run metadata shape, but they do not create compute, log in, or submit jobs.

The referenced Python entrypoints are also skeleton-only:

- `scripts/run_benchmark.py`
- `scripts/run_teacher_evaluator.py`

They write metadata files and produce no benchmark or teacher quality claims until the real harnesses are wired in.
