# Plan: Model Radar Current Release Refresh

## Phase 1: Source Verification

- [x] Task: verify current official/primary-source model availability for the
  newest Hermes, Gemma, Qwen, MiniCPM, and BitNet candidates.
- [x] Task: confirm whether Qwen3.7 has verified open weights.

## Phase 2: Repository Sync

- [x] Task: update `MODEL_CANDIDATES.yaml` with the verified candidates.
- [x] Task: update `FUTURE_MODELS.md` with the refreshed shortlist and guardrail
  text.
- [x] Task: update `HANDOFF.md` with the new radar summary and next-action
  guidance.
- [x] Task: add a concise scan report under `reports/model-radar`.

## Phase 3: Validation

- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: `>= 9.5 / 10`
- Current estimate: `9.6 / 10`
- Evidence: the refresh is strictly additive and keeps speculative models on
  the watchlist.
- Gaps: no runtime proof is claimed for any newly added model.
