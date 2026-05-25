# Hermes Agent mem0 Tool Contract

`scripts/hermes_mem0_tool.py` is the explicit Hermes-agent command surface for
local mem0 reads. It wraps `scripts/mem0_read.py`, keeps the close-margin
reranker as the default, and leaves mem0 defaults unchanged.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/hermes_mem0_tool.py \
  --query "What is the active mem0 Qdrant collection?"
```

Stdin JSON is also supported:

```bash
printf '{"query":"What is the active mem0 Qdrant collection?","cache_ttl_s":300}\n' \
  | ./.venv/bin/python scripts/hermes_mem0_tool.py
```

The checked-in manifest is
`mem0/integration/hermes_agent_mem0_read_tool.json`.

## Contract

- Read-only: true.
- Mutates `~/.mem0/config.json`: false.
- Default mode: `close-margin`.
- Rollback mode: `vector`.
- Experimental mode: `qwen3` with optional `fallback_to_vector`.
- Cache: opt-in TTL, default `300s` for this command wrapper.

Use `refresh_cache: true` after memory writes or when validating a changed
store. Do not wire this as an automatic every-turn prelude; use it as an
explicit or cached memory-read tool.
