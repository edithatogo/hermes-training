# mem0 Guarded Read Wrapper Smoke

Date: 2026-05-26

## Purpose

Validate the agent-facing `scripts/mem0_read.py` entrypoint against the live
local mem0 CLI without writing memories or changing mem0 defaults.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_read.py \
  "What is the active mem0 Qdrant collection?" \
  --tool cmd \
  --mode close-margin \
  --timeout-s 180
```

## Result

| Field | Value |
|---|---:|
| Exit code | 0 |
| Mode | `close-margin` |
| Strategy | `score_plus_created_at_rank_close_margin` |
| Read-only | true |
| Mutates mem0 config | false |
| Input count | 1 |
| mem0 search latency | 2.865s |
| Rerank latency | 0.000s |
| Total latency | 2.865s |

The live default store still returned a singleton result for this query, so the
multi-result quality decision remains the isolated fixture result:
close-margin passed at `1.000`, while Qwen3 0.6B matched vector at `0.667`.

## Decision

Keep `scripts/mem0_read.py` as the guarded agent entrypoint for mem0 reads.
Default to `close-margin`; use `vector` only as rollback/comparison; keep
`qwen3` explicit and experimental until prompt/metadata work fixes the isolated
fixture recency miss.
