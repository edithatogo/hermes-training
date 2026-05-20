# Spec: Frontier Model Radar and Bleeding-Edge Watchlist

## Goal

Keep Hermes Training Hub focused on bleeding-edge models while preventing speculative or unverified releases from becoming ungrounded implementation work.

## Requirements

- Every model must be classified by role, platform environment, and feasibility.
- Verified candidates require a model card, weights or quantization path, license note, runtime path, and benchmark gate.
- Watchlist candidates may be tracked for SOTA awareness but cannot be trained or published until promoted.
- Promotion rules must define the benchmark gate for each role and the publication limit for teacher-only, runtime-only, and watchlist models.
- Include frontier MoE, LFM, Hermes, Qwen, retrieval, recursive, subquadratic, recurrent, ternary, and specialist-runtime families.
- Health target: `>= 9.5 / 10`.

## Acceptance Criteria

- `MODEL_CANDIDATES.yaml` includes role/environment/feasibility fields.
- Speculative models are explicitly marked as watchlist/speculative.
- Model validation skips watchlist entries and checks verified entries.
- Promotion docs name the benchmark gate by role and the publication limit by role.
- Future model docs distinguish verified release candidates from claims to treat carefully.
