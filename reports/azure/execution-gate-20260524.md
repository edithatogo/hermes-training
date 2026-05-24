# Azure Execution Gate

Date: 2026-05-24

## Status

Azure execution status: **blocked for live jobs**

The student Azure account is authenticated and the Azure ML extension is available, but useful modern GPU quota in the checked region remains unavailable. No workspaces, compute clusters, endpoints, or jobs should be created until quota and no-spend gates pass.

## Required Live-Execution Gates

| Gate | Requirement | Current State |
|---|---|---|
| Identity | Active account must be `d.a.mordaunt@gmail.com`. | Passed in read-only preflight. |
| Subscription | Active subscription must be `Azure for Students`. | Passed in read-only preflight. |
| Region | Selected region must be recorded with rationale. | `australiaeast` checked. |
| GPU quota | Useful GPU family quota must be nonzero for the selected SKU/region. | Blocked: sampled T4/A100/H100/A10 rows remain zero. |
| Cost policy | Spot/low-priority, max one node, scale to zero. | Encoded in templates and validator. |
| Workspace | Azure ML workspace may exist only after quota and cost gates pass. | None exists. |
| Compute | Compute must be precreated, low-priority, `min_instances: 0`, `max_instances: 1`. | Templates only. |
| Output sync | Logs/results must sync back under `/Volumes/PortableSSD`. | Required; no live outputs yet. |
| Publication | No claims before synced artifacts and benchmark review. | Blocked. |

## Template Validation

Command:

```bash
source scripts/env.sh
./.venv/bin/python scripts/validate_azure_execution_readiness.py
```

Expected result:

```text
ready: Azure execution templates remain fail-closed
```

## First Allowed Live Action

After useful quota is approved, the first live action should be one minimal benchmark or teacher/evaluator smoke job using the existing dry-run skeleton as the starting point. It should not be a training sweep and it should not create persistent serving infrastructure.

## Publication Boundary

Azure evidence can inform GitHub/Hugging Face only after:

1. job ID, command, logs, and outputs are synced to `/Volumes/PortableSSD`;
2. normalized benchmark summaries exist;
3. the benchmark publication gate passes; and
4. the user explicitly approves publication.
