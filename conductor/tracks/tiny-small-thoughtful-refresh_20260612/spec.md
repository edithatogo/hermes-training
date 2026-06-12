# Specification: Tiny and Small Thoughtful Refresh

## Overview

The Hermes radar needs to keep pace with the tiny and small open-weight tier,
where the newest practical helper and reasoning candidates often appear first.

This refresh focuses on:

- Qwen/Qwen3.5-27B as a dense mid-size teacher
- MiniCPM-V-4.6-Thinking as a multimodal reasoning helper lane
- Nanbeige4.1-3B as a new tiny-model leaderboard candidate

## Scope

- Verify the current published status of the candidate repos.
- Update `MODEL_CANDIDATES.yaml` with the verified candidates.
- Update `FUTURE_MODELS.md` and `HANDOFF.md` with the new guidance.
- Record a concise scan report of the additions and guardrails.

## Out Of Scope

- No runtime proof claims for the new candidates.
- No training runs.
- No promotion of the new models to default local fine-tune targets.

## Acceptance Criteria

- The radar includes the new tiny and small candidates.
- The docs make clear these are runtime, teacher, or helper lanes.
- Qwen3.7 remains watchlist-only.
- Validation passes.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is source-backed and keeps the candidates in
  specialist/runtime lanes.
- Remaining gap: runtime proof is still separate for every candidate.
