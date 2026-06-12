# NVIDIA Physical-AI Follow-Up - 2026-06-12

## Summary

This follow-up scan captures the fresh NVIDIA physical-AI and world-model pages
that are relevant as support lanes for broader Hermes-adjacent workflows.

## Verified Additions

| Family | Verified release | Why it matters |
|---|---|---|
| NVIDIA | `nvidia/instant-nurec` | Physical-AI / synthetic-data generation lane with separate code and weights. |
| NVIDIA | `nvidia/omni-dreams-models` | Action-conditioned world-model lane for simulation and synthetic camera generation. |

## Watchlist Status

- These are support lanes, not Hermes text/chat targets.
- Runtime proof remains a separate gate if these are ever used locally.

## Decision

- Add the new NVIDIA support lanes to `MODEL_CANDIDATES.yaml`.
- Update the radar docs to keep them in the support/runtime bucket.
