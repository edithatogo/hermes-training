# Cloud Gate Preflight - 2026-06-12

This report records the current Azure and NVIDIA/NGC gate state for the Hermes shortlist execution track.

## Azure

- Command: `./.venv/bin/python scripts/azure_preflight.py`
- Result: blocked
- Evidence:
  - Azure CLI is installed.
  - Azure ML CLI extension is installed.
  - SSD artifact root is present.
  - Active account is missing: `Please run 'az login' to setup account.`
- Decision: Azure execution remains gated until the account is logged in and quota/capacity can be checked from the authenticated context.

## NVIDIA / NGC

- Command: `ngc config current`
- Result: no configured API key state was exposed beyond the default table output.
- Decision: NVIDIA jobs remain gated until an explicit NGC API key and model/container availability check are present.

## Specialist Runtime

- Command: `./.venv/bin/python scripts/check_specialist_runtime_preflight.py`
- Result: passed
- Counts:
  - `blocked`: 4
  - `ready-for-smoke`: 1
- Decision: specialist lanes are still pre-smoke only; no lane is promoted by the preflight.

## Summary

The cloud gate is correctly fail-closed. Azure is blocked by missing login, NGC is not yet configured for a usable API-key-backed flow, and the specialist runtime preflight confirms the remaining lanes need native runtimes plus SSD artifacts before smoke work is allowed.
