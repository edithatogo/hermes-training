# Plan: Qwen3 Strict Format Guard V2

## Phase 1 - Data Expansion

- [x] Task: Add deterministic v2 format-guard generator.
- [x] Task: Generate `raw/expansion_seed_v2.jsonl`.
- [x] Task: Materialize deterministic v2 splits.
- [x] Task: Audit raw v2 data and v2 splits.

## Phase 2 - Training And Evaluation

- [x] Task: Add v2 training config.
- [x] Task: Run local Qwen3 4B MLX v2 training.
- [x] Task: Run mirrored and held-out strict tool-call benchmarks for v2.
- [x] Task: Add v3 `/no_think` materializer and training config.
- [x] Task: Run local Qwen3 4B MLX v3 training.
- [x] Task: Run mirrored, held-out, and iteration-80 held-out strict tool-call benchmarks for v3.
- [x] Task: Record publication decision.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10 for implementation rigor and evidence completeness.
- Evidence: v2 and v3 datasets are deterministic and audited, training ran SSD-first, mirrored and held-out benchmark artifacts are recorded, and publication remains blocked by the unchanged strict gate.
- Decision: not publishable. V2 held-out strict pass was `0.250`; v3 held-out strict pass was also `0.250` even though diagnostic empty-think-stripped pass improved to `0.875`.
