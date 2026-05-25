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

## Hermes Plugin Shim

Hermes Agent loads tools through plugins rather than raw JSON manifests. The
safe local wiring path is the user plugin at:

`~/.hermes/plugins/hermes-mem0-read`

The tracked plugin template is `mem0/integration/hermes-mem0-read`. It reads
the checked-in JSON manifest, registers `hermes_mem0_read` under the
`hermes_mem0` toolset, and invokes the command with stdin JSON. This keeps the
dirty `/Volumes/PortableSSD/GitHub/hermes-agent` checkout untouched while still
making the mem0 read wrapper available to Hermes.

Enable or verify it with:

```bash
hermes plugins enable hermes-mem0-read
HERMES_PLUGINS_DEBUG=1 hermes tools list
```

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
