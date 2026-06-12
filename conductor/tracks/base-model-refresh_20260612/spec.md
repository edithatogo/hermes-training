# Specification: Base-Model Release Follow-Up

## Overview

Follow up the 2026-06-12 radar refresh with the newly confirmed official base
repos and packaging lanes that were not yet explicit in the machine-readable
candidate list.

## Scope

- Add `google/gemma-4-31B` as an explicit base-model teacher lane.
- Add `Qwen/Qwen3-Coder-Next` as the official subquadratic base behind the GGUF
  runtime lane.
- Add `openbmb/MiniCPM-V-4.6-GPTQ` as an explicit local packaging comparison
  point.
- Update the model radar docs and scan notes to mention the new base repos and
  keep `Qwen3.7` watchlist-only.

## Out Of Scope

- No runtime proof.
- No training or benchmark claims.
- No publication or adapter promotion.

## Acceptance Criteria

- The machine-readable candidate list includes the new base repos.
- The human-readable radar docs mention the follow-up scan.
- Validation passes cleanly.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the additions are official, source-backed repositories with clear
  Hermes-adjacent relevance.
- Remaining gap: runtime proof remains a separate gate.
