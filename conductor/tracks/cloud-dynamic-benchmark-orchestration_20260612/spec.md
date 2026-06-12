# Cloud Dynamic Benchmark Orchestration

## Overview

Build a dynamic orchestration lane that moves suitable model benchmark and smoke tasks off the local Mac and onto external runtimes, with Colab CLI as the first target and Azure/NVIDIA routes gated by real authentication, quota, entitlement, and cost checks.

## Current Preflight State

- Colab CLI is installed as `/Users/doughnut/.local/bin/colab`.
- `colab sessions` succeeds and currently reports no active sessions.
- Colab CLI reports an available update from 0.5.9 to 0.5.11.
- Azure CLI is installed as `/opt/homebrew/bin/az`, but `az account show` currently requires `az login`.
- NVIDIA NGC CLI is installed as `/usr/local/bin/ngc`, but `ngc config current` shows only default config and no configured API key.
- Kaggle CLI was not found on PATH during the preflight check.

## Scope

- Create reusable job definitions for model smoke tests, benchmark slices, embedding/reranker comparisons, and runtime proof jobs.
- Prefer Colab for sanitized, bounded jobs that are expensive locally.
- Parallelize independent candidate jobs while respecting local storage, remote runtime limits, and rate limits.
- Gate Azure usage behind login, subscription, region, quota, and cost checks.
- Gate NVIDIA/NGC usage behind API key, org/team, entitlement, container/model availability, and license checks.
- Add Kaggle only after CLI availability and auth are confirmed.
- Preserve local reproducibility by storing commands, scripts, result summaries, and environment notes.

## Out of Scope

- Uploading private memory data, secrets, or restricted datasets to cloud runtimes.
- Running paid GPU jobs without explicit cost approval.
- Keeping remote sessions alive after jobs complete.
- Replacing local Mac/Metal proof for candidates that must run on the current system.

## Acceptance Criteria

- A runner/operator can select local, Colab, Azure, NGC, or future Kaggle routes from a single documented workflow.
- Colab jobs can be launched, monitored, summarized, and cleaned up from the CLI.
- Azure and NGC jobs fail closed when auth, quota, entitlement, or cost checks are missing.
- Parallel jobs are bounded by candidate priority, data safety, and runtime capacity.
- Results flow back into benchmark reports and candidate metadata without large unreviewed artifacts.

## Health Target

This track should not be marked complete below health 9.5. Completion requires a working Colab path and documented blocked/prepared state for Azure, NGC, and Kaggle.
