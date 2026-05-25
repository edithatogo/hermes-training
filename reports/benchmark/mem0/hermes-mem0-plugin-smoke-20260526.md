# Hermes mem0 Plugin Smoke

Date: 2026-05-26

## Purpose

Validate the installed Hermes user plugin at
`~/.hermes/plugins/hermes-mem0-read` after enabling it in
`~/.hermes/config.yaml`.

## Commands

```bash
HERMES_PLUGINS_DEBUG=1 hermes tools list
```

`hermes tools list` loaded `hermes-mem0-read`, registered
`hermes_mem0_read`, and exposed the `hermes_mem0` plugin toolset.

The plugin handler was then imported directly and invoked through its default
close-margin mode:

```bash
PYTHONPATH=/Volumes/PortableSSD/GitHub/hermes-agent python3 - <<'PY'
import importlib.util
from pathlib import Path

path = Path("/Volumes/PortableSSD/appdata/hermes/plugins/hermes-mem0-read/__init__.py")
spec = importlib.util.spec_from_file_location("hermes_mem0_read_plugin", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
result = mod._handle_mem0_read(
    query="What is the active mem0 Qdrant collection?",
    mode="close-margin",
    cache_ttl_s=300,
    fallback_to_vector=True,
)
print(result)
PY
```

## Result

| Metric | Value |
|---|---:|
| Plugin enabled | true |
| Toolset visible | `hermes_mem0` |
| Tool registered | `hermes_mem0_read` |
| `ok` | true |
| Read-only | true |
| Mutates mem0 config | false |
| Mode | `close-margin` |
| Strategy | `score_plus_created_at_rank_close_margin` |
| Cache hit | false |
| Memories returned | 1 |
| Total latency | 3.970s |
| mem0 search latency | 3.968s |
| Rerank latency | 0.000s |

## Decision

The plugin shim is ready for explicit Hermes memory reads. Keep the tool
explicit/cached rather than automatic on every turn, and keep the
`/Volumes/PortableSSD/GitHub/hermes-agent` checkout untouched until its local
dirty edits are preserved.
